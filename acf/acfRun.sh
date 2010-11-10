#!/bin/bash

usage() 
{
    cat <<-EOF >&2

    usage: ./${0##*/} [-r RELEASE:BOARD] [-m MODULE] [-v CCVIEW|local] [-s SETTINGSFILE] [-c CONFIGSPEC] [-d DRIVER] [-K DEFCONFIGS_PATH]

    -r Release:Board		Release and Board
    -m Module			Module to compile, x-load|u-boot|kernel|testsuites
    -v CC view			ClearCase View
    -s Settings			Settings file
    -c Config Spec [Optional]	Specify a specific config spec
    -K Path [Optional]		Directory with configuration files for multiple kernel builds

    example: ./${0##*/} -r 12x:3430 -m kernel -v omapsw_x0066660_auto -s ~/settingsfile

		EOF
		exit 0
}

main()
{

	if [ $# -le 4 ] 
	then
		usage
		exit 1
	fi

	while getopts h:r:m:v:s:c:K: arg
  do case $arg in
    	
  h) usage;;
    	
	r) RELEASE=${OPTARG%:*}
	BOARD=${OPTARG#*:}
	DEFCONFIGSDIRECTORY="default"
	release_test=`echo $RELEASE | grep "^[A-Za-z0-9]*[x][*]*$"`
	if [ -z "$release_test" ] ; then
		MAJOR_NUMBER=`echo $RELEASE | sed -ne "s%\([0-9]*\)[x]\([0-9X]*\).*%\1%gp"`
		MINOR_NUMBER=`echo $RELEASE | sed -ne "s%\([0-9]*\)[x]\([0-9X]*\).*%\2%gp"`
		RELEASECC=${MAJOR_NUMBER}.${MINOR_NUMBER}
		MAINRELEASE=${MAJOR_NUMBER}x
	  VOB=/vobs/wtbu
	  VOB_DOCUMENTS=$VOB/csdoc/Programs/$BOARD/SW/Linux_$MAJOR_NUMBER.x/Config_Specs
	else
		MAINRELEASE=$RELEASE
	fi
	
	DRIVER="generic";;

	m) MODULES=$OPTARG;;
	v) VIEW=$OPTARG
	
	if [ ! $VIEW == "local" ] ; then
		CLEARTOOL=/usr/atria/bin/cleartool
		BUILDVIEW=`$CLEARTOOL lsview -short $VIEW`
		if [ $? -ne 0 ] ; then
			echo "Wrong view name -> $VIEW"
			exit 1
		fi
		TESTFRAMEWORKVIEW=`$CLEARTOOL pwv -short`
		export ROOT=`pwd`
		export ACFROOT=/view/$TESTFRAMEWORKVIEW/$ROOT
	else
		export ACFROOT=`pwd`
	fi
	
	export ACFCONF=$ACFROOT/../conf
	export ACFSPECS=$ACFROOT/../conf/configspecs/
	export PYTHONPATH=$PYTHONPATH:$ACFROOT/../lib/
	#source $ACFROOT/../lib/TIToolChain.sh
  
  if [ -z "$release_test" ] ; then
  	CONFIGSPEC=/view/${VIEW}/$VOB_DOCUMENTS/Linux_${RELEASECC}_release_cs.txt
  else
		CONFIGSPEC=$ACFSPECS/$RELEASE
	fi;;
			
	s) SETTINGS=$OPTARG
	[ -e $OPTARG ] ||
	{
        	echo "FATAL: Settings file not found"
        	exit 1
	};;
			
	c) if [ ! $OPTARG == "none" ] ; then
		CONFIGSPEC=$OPTARG
	fi;;
	
	K) if [ ! $OPTARG == "none" ] ; then 
		DEFCONFIGSDIRECTORY=$OPTARG
	else
		DEFCONFIGSDIRECTORY="default"
	fi;;					
			
	\?) usage;;
	
	esac
	done
	
	if [ ! $VIEW == "local" ] ; then

		$CLEARTOOL startview $VIEW
		[ -e $CONFIGSPEC ] ||
  	{
  		echo ; echo "FATAL: Config Spec file not found" 
  		echo "Using the following Release & Platform : $RELEASE:$BOARD"
  		echo "Please verify!!!" ; echo
    	exit 1
  	}
		$CLEARTOOL setcs -tag $VIEW $CONFIGSPEC  	
  	$CLEARTOOL endview $VIEW
		cd $ACFROOT
		$CLEARTOOL setview -login -exec "$ACFROOT/acfMain.py $MAINRELEASE:$RELEASE:$BOARD $MODULES $SETTINGS $CONFIGSPEC $VIEW $TESTFRAMEWORKVIEW $DEFCONFIGSDIRECTORY" $VIEW	 
	else
		$ACFROOT/acfMain.py $MAINRELEASE:$RELEASE:$BOARD $MODULES $SETTINGS $CONFIGSPEC local nothing $DEFCONFIGSDIRECTORY
	fi

}

main "$@"
