#!/bin/bash

# Linux Base Port Test Team - Automated Test Framework
# Mark Hattarki <hattarki@ti.com> 
# Texas Instruments, All Rights Reserved 2007
#
# Description
# 
	# Automated Test Framework requires 4 arguments
	# First argument  : [auto][manual][utr][sst]
	# Second argument : [release]
	# Third argument 	: [compile][boot][both]
	# Fourth argument : [path to driver's file]


mainbanner()
{

	echo
	echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
	echo "A U T O M A T E D   T E S T   F R A M E W O R K"
	echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
	echo
	echo "User    : $USERNAME"
	echo "Release : $RELEASE"
	echo "Board 	: $BOARD"
	echo
	echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
	echo
	    
	    
}


setup()
{
	
	export ATFROOT=`pwd`
	export ATFBIN=$ATFROOT/../bin
	export ATFCONF=$ATFROOT/../conf
	export ATFSPECS=$ATFROOT/../conf/configspecs/
	export PYTHONPATH=$PYTHONPATH:$ATFROOT/../lib/
	export USERNAME=$(id -un)

}

usage() 
{
    cat <<-EOF >&2

    usage: ./${0##*/} [-r RELEASE:BOARD] [-t TESTING] [-s SETTINGSFILE] [-c CONFIGSPEC]
	
    -r Release:Board	Release and Board
    -t Testing      	What to be tested? Auto, Manual, Stress
    -s Settings     	Settings file
    -c Config Spec	Specify a specific config spec

    example: ./${0##*/} -r 12x:3430 -t auto -s ~/settingsfile

		EOF
		exit 0
}


main()
{

	if [ "$#" == 0 ] 
	then
		usage
		exit 1
	fi
	
	export CONFIGSPEC="none"
		
	while getopts h:r:t:s:c: arg
  	do case $arg in
    	
    	h) usage;;
    	
			r) RELEASE=${OPTARG%:*}
					BOARD=${OPTARG#*:}
				 	CONFIGSPEC="None"
					release_test=`echo $RELEASE | grep "^[A-Za-z0-9]*[x][*]*$"`
					
					if [ -z "$release_test" ] ; then
				 	
					 	MAJOR_NUMBER=`echo $RELEASE | sed -ne "s%\([0-9]*\)[x]\([0-9X]*\).*%\1%gp"`
					 	MINOR_NUMBER=`echo $RELEASE | sed -ne "s%\([0-9]*\)[x]\([0-9X]*\).*%\2%gp"`
					 	RELEASECC=${MAJOR_NUMBER}.${MINOR_NUMBER}
					 	MAINRELEASE=${MAJOR_NUMBER}x
	  				
					else
	
						MAINRELEASE=$RELEASE
	  			
	  			fi
				 	
				 	DRIVER="generic";;
		 	
			
			t) TESTING=$OPTARG;;
			
			s) SETTINGS=$OPTARG
					[ -e $OPTARG ] ||
    			{
        		echo "FATAL: Settings file not found"
        		exit 1
        	};;
			
			c) CONFIGSPEC=$OPTARG
					[ -e $OPTARG ] ||
    			{
	        	echo "FATAL: config Spec file not found"
	        	exit 1
  	      };;
			
			\?) usage;;
			esac
		done
	
	mainbanner
	$ATFROOT/atfMain.py $MAINRELEASE:$RELEASE:$BOARD $TESTING $SETTINGS $CONFIGSPEC
	
}

setup
main "$@"
