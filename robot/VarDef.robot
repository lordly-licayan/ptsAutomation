*** Variables ***
${SERVER1}		    			URL_HERE
${SERVER2}		    			URL_HERE
${SERVER3}		    			URL_HERE
${SERVER4}		    			URL_HERE
${SERVER5}		    			URL_HERE
			
${BROWSER}		    			ie
${ON}			    			True
${OFF}			    			False
			
${DEFAULT_RETRY}    			5 sec
${DEFAULT_RETRY_INTERVAL}       1 sec

${SVRIP}                        IP
${SVR66}                        ${SVRIP}\\66\\file
${SVR77}                        ${SVRIP}\\77\\file
${SVR88}                        ${SVRIP}\\88\\file
${INI_FILENAME}                 filename.ini
${LOCAL_INI_PATH}               ${OUTPUTDIR}\\..
${ORIG_INI_PATH}                ${SVR66}