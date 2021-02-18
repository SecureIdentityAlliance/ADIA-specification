README.txt
 To generate new password hash use this command line (PERL):

    perl -le 'print crypt("password", "didalliance-salt")'

 Then modify the htpasswd file adding the new user using this structure:

  {user_name}:{generated_password}
