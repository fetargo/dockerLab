#!/bin/bash
if ! [ $(id -u) = 0 ]
then
   echo "Error: This script needs root permitions" >&2
   exit 1
fi
echo -e "Program: Mini-admin\nCreator: Yashin Aleksey 727-1 \nThis is mini administration tool that allows you to change user's:\n- password expire date;\n- command shell; \n- home directory"
echo "Registered users: "
cat /etc/passwd | sed 's/:.*//'
error=0
while true
do
    echo -n "Press Enter to quit or enter username for administration: "
    read username
    if [ -z "$username" ]
       then
       echo "Closing program..."
       exit $error
    elif ! cat /etc/passwd | sed 's/:.*//' | grep -w $username
       then
   	echo "User $username does not exist" >&2
   	error=2
   	continue
    else
    	error=0
   	break
    fi
done
while true
do
   echo -e "Administrating user $username \nChoose action: \n1 to change password expire date;\n2 to change command shell;\n3 to change home directory;\n4 to change user;\n5 to exit programm."
   read chose
   case $chose in
      1)
   	   echo -n "Enter number of days to $username pass expire: "
	   read days
	   case $days in
    	   ''|*[!0-9]*)
    	    	 echo "Error: You must enter the number" >&2
    	    	 error=3
	      	 continue ;;
    	   *) 
    	   	passwd -x $days $username
	      	echo "Password will expire in $days days" 
	      	error=0;;
	   esac ;;
      2)
	   echo -e "Choose command shell for $username: \n1 - /bin/sh;\n2 - /bin/bash;\n3 - /sbin/nologin;\nAny else key - back."
	   error=0
	   read num
	   case $num in
		1) 
		    usermod -s /bin/sh $username
		    echo "/bin/sh is now a command shell for user 				$username";;
		2) 
		    usermod -s /bin/bash $username
                    echo "/bin/bash is now a command shell for user 				$username";;
		3) 
		    usermod -s /sbin/nologin $username
                    echo "/sbin/nologin is now a command shell for user 				$username";;
		*)  
		    continue;;
	   esac;;
      3)
      	   if users | grep -w $username 
      	        then
      	   	echo "Error: user $username is logged in. You must log off this user first" >&2
      	   	error=4
      	   	continue
      	   else
	   	echo "Enter new home directory for $username:"
	   	read path
	   	usermod -md $path $username
	   	chown $username $path
	   	echo "$username home directory is now $path"
	   	error=0
	   fi;;
      4)  
      	   while true
      	   do
	       echo "Registered users: "
	       cat /etc/passwd | sed 's/:.*//'
	       echo -n "Press Enter to administrate previous user or enter new username for administration: "
	       read newusername
   	       if [ -z "$newusername" ]
   	          then
   	          break
   	       elif ! cat /etc/passwd | sed 's/:.*//' | grep -w $newusername
   	          then
   	          echo "User $newusername does not exist" >&2
   	          error=2
   	          continue
	       else
	          username=$newusername
   	          break
   	          error=0
   	       fi
	   done;;
	5) 
	   echo "Closing program..."
	   exit $error;;
	esac
	   
done
exit $error
