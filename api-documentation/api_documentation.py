*******************************************************************************************************************************************************************


<<GET REQUESTS>>


*Searching for an Account/user using ID's*

	3 Account Types:
		-user
		-parent
		-teacher

Instructions are given below.	


How to use ...												


 ___________________________________________________________________________________________________________________________
|		ROUTES				|								FUNCTION														|
|___________________________|_______________________________________________________________________________________________|
|	/api/users        		|		# return all jasonified data about the user from the table								|													
|	/api/user/<acc_id>		|		# return a jasonified details about the user using the user's account ID <acc_id>		|
|	/api/parent/<acc_id>	|		# return a jasonified details about the parent using the user's account ID <acc_id>		|
|	/api/teacher/<acc_id>	|		# return a jasonified details about the teacher using the user's account ID <acc_id>	|
-----------------------------------------------------------------------------------------------------------------------------


Note: If the account ID <acc_id> inputed does not exist, it will return an error message
	 
	 >>>{'message': "no user found"}




		example:

			input:
				>>https://mighty-badlands-16603.herokuapp.com/api/user/1

			result:

				user:
				[
					{
						acc_id: 1
						username: User Numbowan
						email: sample@email.com
						acc_type: Parent
					}
				]

***GET the details about the Child***
	
How to use ...

	<<</api/child/<c_id>>>>   #return the  details about the child using the child ID <c_id>

		example:

			input:
				>>https://mighty-badlands-16603.herokuapp.com/api/child/1

			result:

				user:
				[
					{
						fname_c: Dough
						lname_c: Ware
						bday_c: 06/08/98
						diagnosis: ADHD
					}
				]


[Go on & Try it]




*******************************************************************************************************************************************************************


<<POST REQUESTS>>

 ___________________________________________________________________________________________________________________________
|		ROUTES				|								FUNCTION														|
|___________________________|_______________________________________________________________________________________________|
|	/api/signup        		|		# It will be use to register as a user													|													
|	/api/add_class			|		# It will be use to add a Class 														|
|	/api/add_directory		|		# It will be use to add a new contact in the directory									|
|	--				--		|		# return a jasonified details about the teacher using the user's account ID <acc_id>	|
-----------------------------------------------------------------------------------------------------------------------------


Note: You can use postman,python-requests,ajax and etc ... to make a post request on this routes


***POST to register as a user***

	<<</api/signup>>> # this will be use to post request when some wants to register as a user
	

		example:

			request on:

				>>>https://mighty-badlands-16603.herokuapp.com/api/signup

			
			expected result/response:

				>>>{'message': 'New user created.'}


***POST to add a Class for the students***

	<<</api/add_class>>> 

		example:

			request on:

				>>>https://mighty-badlands-16603.herokuapp.com/api/add_class

			expected result/response:

				>>>{'message' : 'New Class created.'} #not yet edited, it will return {'message': 'New user created.'}



***POST to add a contact to the directory***

	<<</api/add_directory>>> 

		example:

			request on:

				>>>https://mighty-badlands-16603.herokuapp.com/api/add_directory

			expected result/response:

				>>>{'message' : 'New contact added.'}

******************************************************************************************************************************************************************