#!/bin/bash


usage() 
{
    cat <<-EOF >&2

    usage: ./${0##*/} [-x PRIMARY CONFIG SPEC] [-y SECONDARY CONFIG SPEC] [-m ] {x-load | u-boot | kernel}  [-b BOARD] [-s SETTINGS]
	
    -x Primary     	Primary Config Spec to use
    -y Secondary	Secondary Config Spec to use
    -m module		Module {x-load | u-boot | kernel}
    -b board		Board to use    
    -s Settings     	Settings file
						
		example: ./${0##*/} -x 12x9 -y 12x -m kernel -b 3430 -s ~/settings
		Note. Differences Framework will work only wihtin a Clear Case Environment

		EOF
		exit 0
}


setup()
{
  CLEARTOOL=/usr/atria/bin/cleartool
	TESTFRAMEWORKVIEW=`$CLEARTOOL pwv -short`
	export ROOT=`pwd`
	export ADFROOT=/view/$TESTFRAMEWORKVIEW/$ROOT
	export ADFCONF=$ADFROOT/../conf
	export ADFSPECS=$ADFROOT/../conf/configspecs/
  export PYTHONPATH=$PYTHONPATH:$ADFROOT/../lib/
  cd $ADFROOT
}

createView()
{
	if $CLEARTOOL lsview -short $1 2>/dev/null >/dev/null; then
		echo "$Clear Case View exists..."
		$CLEARTOOL rmview -tag $1
	fi
	if ! /usr/local/bin/mkview_linked $1 ; then
		echo "Failed to create Clear Case View $1"
		exit 1
	fi
}

buildconfigspecinfo()
{
					release_test=`echo $1 | grep "^[A-Za-z0-9]*[x][*]*$"`					
					if [ -z "$release_test" ] ; then
					 	MAJOR_NUMBER=`echo $1 | sed -ne "s%\([0-9]*\)[x]\([0-9X]*\).*%\1%gp"`
					 	MINOR_NUMBER=`echo $1 | sed -ne "s%\([0-9]*\)[x]\([0-9X]*\).*%\2%gp"`
					 	RELEASECC=${MAJOR_NUMBER}.${MINOR_NUMBER}
					 	MAINRELEASE=${MAJOR_NUMBER}x
	  				VOB=/vobs/wtbu
	  				VOB_DOCUMENTS=$VOB/csdoc/Programs/$BOARD/SW/Linux_$MAJOR_NUMBER.x/Config_Specs
					else
						CONFIGSPEC=$ADFSPECS/$1
	  			fi
}

setconfigspec()
{
	$CLEARTOOL startview $1
	if [ -z "$release_test" ] ; then
		CONFIGSPEC=/view/${1}/$VOB_DOCUMENTS/Linux_${RELEASECC}_release_cs.txt
	fi
	
	[ -e $CONFIGSPEC ] ||
  {
  	echo "FATAL: Config Spec file not found"
    exit 1
  }
	$CLEARTOOL setcs -tag $1 $CONFIGSPEC
}

main()
{

	if [ "$#" == 0 ] 
	then
		usage
		exit 1
	fi

	while getopts h:x:y:s:b:m: arg
  	do case $arg in
    	
    	h) usage;;
    	
			x) PRIMARY=$OPTARG
						PMAJOR_NUMBER=`echo $PRIMARY | sed -ne "s%\([0-9]*\)[x]\([0-9X]*\).*%\1%gp"`
					 	PMAINRELEASE=${PMAJOR_NUMBER}x			
					;;
							
			y) SECONDARY=$OPTARG
					SMAJOR_NUMBER=`echo $SECONDARY | sed -ne "s%\([0-9]*\)[x]\([0-9X]*\).*%\1%gp"`
					SMAINRELEASE=${SMAJOR_NUMBER}x
					;;
			
			m) MODULE=$OPTARG
					;;
			
			s) SETTINGS=$OPTARG
					[ -e $OPTARG ] ||
    			{
        		echo "FATAL: Settings file not found"
        		exit 1
        	};;
			
			b) BOARD=$OPTARG;;        	
	
		
			\?) usage;;
			esac
		done

	if [ $PRIMARY == $SECONDARY ]
	then
		echo "Primary Release is equal to Secondary Release"
		echo "Cannot continue"
		exit 1
	fi
	
	PRIMARYVIEW="omapsw_`id -un`_${PRIMARY}diff"
	createView $PRIMARYVIEW
	buildconfigspecinfo $PRIMARY
	setconfigspec $PRIMARYVIEW

	SECONDARYVIEW="omapsw_`id -un`_${SECONDARY}diff"
	createView $SECONDARYVIEW
	buildconfigspecinfo $SECONDARY
	setconfigspec $SECONDARYVIEW
	
	echo
	$CLEARTOOL setview -login -exec "$ADFROOT/adfMain.py $PMAINRELEASE:$PRIMARY $SMAINRELEASE:$SECONDARY $MODULE $SETTINGS $BOARD" $PRIMARYVIEW
	echo
	
	cd $ADFROOT
	
	if ! $CLEARTOOL rmview -tag $PRIMARYVIEW; then
  	echo "Failed to delete $PRIMARY_VIEW"
    exit 1
  fi
  
	if ! $CLEARTOOL rmview -tag $SECONDARYVIEW; then
  	echo "Failed to delete $PRIMARY_VIEW"
    exit 1
  fi
  echo
}

setup
main "$@"

