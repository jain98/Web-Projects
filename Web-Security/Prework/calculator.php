<!DOCTYPE html>

<?php
     ini_set('display_errors',0);
     if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $total = $_POST["total"];
        $tip = $_POST["tip_percentage"];
        $new_tip = calculate_tip($total, $tip);
        $new_total = $total + $new_tip;
     }

     function calculate_tip($total, $tip) {
        return (($tip / 100) * $total);
     }
?>

<html>
  <head>
    <meta charset="utf-8">
    <title>Calculator</title>
    <!-- Bootstrap -->
    <link href="static/css/bootstrap.min.css" rel="stylesheet" >
    <link href="static/css/bootstrap-theme.min.css" rel="stylesheet">
    <link href="static/css/font-awesome.min.css" rel="stylesheet">
    <link href="static/css/bootstrap-social.css" rel="stylesheet">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  </head>

  <script type="text/javascript">
    $(document).ready(function(){
      $('#tip_div').style.height = '500px';
      $('#submit').click(function(){
        $('#tip_div').style.height = '700px';
      });
    });
  </script>

  <body>
    <br>
    <div class="container" id="tip_div" style="width:300px; border:1px solid #000; text-align:left;">
      <h1>Tip Calculator</h1>
      <form class="form-inline" action="calculator.php" method="post" style="padding:10px;">
        <br>
        <div class="form-group">
          <label for="total" class="control-label">Bill subtotal: $</label>
          <input type="number" class="form-control" name="total" value="<?php if(isset($new_total)) {echo $total;} else {echo 1;}?>" style="width: 90px;" min="1" required>
        </div>
        <br><br>
        <div class="form-group">
          <label for="tip_percentage" class="control-label">Tip Percentage:</label><br>
          <input type="radio" class="form-control" name="tip_percentage" value="10%" checked="checked"> 10% &nbsp;&nbsp;
          <input type="radio" class="form-control" name="tip_percentage" value="15%"> 15% &nbsp;&nbsp;
          <input type="radio" class="form-control" name="tip_percentage" value="20%"> 20%
        </div>
        <br><br>
        <button type="submit" id="submit" class="btn btn-primary">Submit&nbsp;<span class="fa fa-calculator"></span></button>
      </form>
      <div class="container" style="width:150px; height:100px; border:1px solid #000; text-align:left; display:<?php echo $new_total > 0 ? 'block':'none'?>">
        <p>Tip: &nbsp;&nbsp;$ <?php echo round($new_tip,2);?></p>
        <br><br>
        <p>Total: &nbsp;&nbsp;$ <?php echo round($new_total,2);?></p>
      </div>
      <br>
    </div>

  </body>
</html>
