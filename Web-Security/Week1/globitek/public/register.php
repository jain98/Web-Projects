<?php
  require_once('../private/initialize.php');
  // include '../private/functions.php';
  // include '../private/validation_functions.php';

  // Set default values for all variables the page needs.
  $first_name = '';
  $last_name = '';
  $email = '';
  $username = '';
  $errors = [];

  // if this is a POST request, process the form
  if(is_post_request())
  {
    // Confirm that POST values are present before accessing them.
    $first_name = isset($_POST['fname']) ? $_POST['fname'] : '';
    $last_name = isset($_POST['lname']) ? $_POST['lname'] : '';
    $email = isset($_POST['email']) ? $_POST['email'] : '';
    $username = isset($_POST['uname']) ? $_POST['uname'] : '';

    // Perform Validations
    if(is_blank($first_name)){
      $errors[] = 'First name cannot be blank.';
    }
    else
    {
      if(!has_length($first_name,['min' => 2, 'max' => 255]))
      {
        $errors[] = 'First name must be between 2 and 255 characters.';
      }
    }

    if(is_blank($last_name)){
      $errors[] = 'Last name cannot be blank.';
    }
    else
    {
      if(!has_length($last_name,['min' => 2, 'max' => 255]))
      {
        $errors[] = 'Last name must be between 2 and 255 characters.';
      }
    }


    if(is_blank($email)){
      $errors[] = 'Email cannot be blank.';
    }
    else
    {
      if(!has_length($email,['max' => 255]))
      {
        $errors[] = 'Email must be less than 255 characters.';
      }
      if(!has_valid_email_format($email))
      {
        $errors[] = 'Email must be a valid format.';
      }
    }

    if(is_blank($username))
    {
      $errors[] = 'Username cannot be blank.';
    }
    else
    {
      if(!has_length($username,['min' => 8, 'max' => 255]))
      {
        $errors[] = 'Username must be between 8 and 255 characters.';
      }
    }



    // if there were no errors, submit data to database
    if(empty($errors))
    {
      // Write SQL INSERT statement
      $datetime = date("Y-m-d H:i:s");
      $sql = "INSERT INTO users (first_name, last_name, email, username, created_at)
              VALUES('$first_name', '$last_name', '$email', '$username', '$datetime')";

      // For INSERT statments, $result is just true/false
      $result = db_query($db, $sql);
      if($result)
      {
         db_close($db);
         header("Location: registration_success.php");
         exit;
      }
      else {
        // The SQL INSERT statement failed.
        // Just show the error, not the form
        echo db_error($db);
        db_close($db);
        exit;
      }
    }
  }
?>

<?php $page_title = 'Register'; ?>
<?php include(SHARED_PATH . '/header.php'); ?>

<div id="main-content">
  <h1>Register</h1>
  <p>Register to become a Globitek Partner.</p>

  <?php
    if($errors !== []){
      echo display_errors($errors);
    }
  ?>

  <!-- TODO: HTML form goes here -->
  <form action="register.php" method="post">
    First name: <br>
    <input type="text" name="fname" value="<?php echo $first_name; ?>" /><br>
    Last name: <br>
    <input type="text" name="lname" value="<?php echo $last_name; ?>" /><br />
    Email: <br>
    <input type="text" name="email" value="<?php echo $email; ?>" /><br />
    Username: <br>
    <input type="text" name="uname" value="<?php echo $username; ?>" /><br />
    <br />
    <input type="submit" name="submit" value="Submit" />
  </form>
</div>

<?php include(SHARED_PATH . '/footer.php'); ?>
