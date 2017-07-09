<?php
require_once('../../../private/initialize.php');
$errors = array();
$territory = array(
  'name' => '',
  'position' => '',
  'state_id' => ''
);


if(is_post_request()) {
  $territory['state_id'] = htmlentities($_POST['state_id']);
  $id = htmlentities($_POST['state_id']);
  // Confirm that values are present before accessing them.
  if(isset($_POST['name'])) { $territory['name'] = htmlentities($_POST['name']); }
  if(isset($_POST['position'])) { $territory['position'] = htmlentities($_POST['position']); }

  $result = insert_territory($territory);
  if($result === true) {
    $new_id = db_insert_id($db);
    redirect_to('show.php?id=' . $new_id);
  } else {
    $errors = $result;
  }
}
else{
  $id = $_GET['id'];
}
?>

<?php $page_title = 'Staff: New Territory'; ?>
<?php include(SHARED_PATH . '/header.php'); ?>

<div id="main-content">
  <a href="../states/show.php?id=<?php echo $id; ?>">Back to State Details</a><br />

  <h1>New Territory</h1>

  <!-- TODO add form -->
  <?php echo display_errors($errors); ?>
  <form action="new.php" method="post">
    Name:<br />
    <input type="text" name="name" value="<?php echo $territory['name']; ?>" /><br />
    Position:<br />
    <input type="text" name="position" value="<?php echo $territory['position']; ?>" /><br />
    <br />
    <input type="text" name="state_id" value="<?php echo $id; ?>" hidden="true">

    <input type="submit" name="submit" value="Create"  />
  </form>

</div>

<?php include(SHARED_PATH . '/footer.php'); ?>
