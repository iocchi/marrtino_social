<!DOCTYPE html>
<html>

<head>


  <meta charset="utf-8" />
  <title>MARRtino Social User Interface</title>
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
  <script src="https://meet.jit.si/external_api.js"></script>
  <script src="js/jquery-3.4.1.min.js"></script>
  <script src="bootstrap/js/bootstrap.min.js"></script>
  <script type="text/javascript" src="js/roslib.min.js"></script>
   <script type="text/javascript" src="js/eventemitter2.min.js"></script>
  <script type="text/javascript" src="js/keyboardteleop.min.js"></script>
  <script type="text/javascript" type="text/javascript">
    var teleop;
    var ros = new ROSLIB.Ros({
      url: 'ws:' + window.location.hostname +':9090'
    });

    ros.on('connection', function () {
      document.getElementById("status").innerHTML = "Connected";
    });

    ros.on('error', function (error) {
      document.getElementById("status").innerHTML = "Error";
    });

    ros.on('close', function () {
      document.getElementById("status").innerHTML = "Closed";
    });

      

     
	
    window.onload = function () {
	  
      
	  
    }

  </script>
  
<style>

.container {
  position: relative;
}

</style>
</head>

<body>
<?php include "nav.php" ?>

<div class="container">
      <h3> </h3>
    
      
      <div class="row">
        <div class="col-md-1"></div>
        <div class="col-md-4">
          <div class="thumbnail">
            <a href="https://www.robotics-3d.com">
              <img style="display: block;margin-left: auto;margin-right: auto;" src="image/LogoRobotics.png" alt="robotics-3d.com"width="40%">
    
            </a>
          </div>
        </div>

        <div class="col-md-2">  </div>
        <div class="col-md-4">
          <div class="thumbnail">
            <a href="https://robotics.surfweb.eu" target="_blank">
              <img style="display: block;margin-left: auto;margin-right: auto;" src="image/LogoCircolareATNero.png" alt="artigianitecnologici.it" width="40%">
              
            </a>
          </div>
        </div>
        <div class="col-md-1">  </div>
      </div>
  
          <div class="row">
            <div class="col-md-4">
              <div class="card mb-4 box-shadow">

                <a  href="../bringup/index.html">
                <img class="card-img-top" src="image/bringup.png" width="50%" alt="bringup">
                 </a>

                <div class="card-body">
                  <p class="card-text">In this section you can start MARRtina Social or a simulators and their services, such as sensors or actuators.</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                       
                      <a class="btn btn-primary" href="../bringup/index.php" role="button">BRINGUP</a>
                    </div>
                   
                  </div>
                </div>
              </div>
            </div> 
            <div class="col-md-4">
              <div class="card mb-4 box-shadow"> 
                <a  href="facerobot.php">
                <img class="card-img-top" src="image/SocialInterface.png" alt="Marrtina">
                 </a>
                <div class="card-body">
                  <p class="card-text">In this section you can start  Social interface Marrtino Robot.</br></br></p>
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                      
                       <a class="btn btn-primary" href="facerobot.php" role="button"> Social Interface</a>
                    </div>
                    
                  </div>
                </div>
              </div>
            </div>
            <h3> </h3>
    
            <div class="col-md-4">
              <div class="card mb-4 box-shadow"> 
                <a  href="../chess">
                <img class="card-img-top" src="image/Marrtino.jpg" alt="Scacchi">
                 </a>
                <div class="card-body">
                  <p class="card-text">In this section you can start MARRtino or a simulators and their services, such as sensors or actuators.</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                        <?php    
                          $mylink =  $_SERVER['HTTP_HOST'];
                          $mylink = "http://" . substr($mylink,0, strpos($mylink,":8080"));
                             ?>
                       <a class="btn btn-primary" href="<?php echo $mylink;?>" role="button">MARRtino ROBOT</a>
                    </div>
                    
                  </div>
                </div>
              </div>
            </div>
            
          


</div>

 
  <div class="row">
           
            <div class="col-md-4">
              <div class="card mb-4 box-shadow"> 
                <a  href="../program/index.html">
                <img class="card-img-top" src="image/Programming.png" alt="Marrtina">
                 </a>
                <div class="card-body">
                  <p class="card-text">Program interface Marrtino Robot.</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                      
                       <a class="btn btn-primary" href="../program/index.html" role="button">Program Interface</a>
                    </div>
                    
                  </div>
                </div>
              </div>
            </div>
            <h3> </h3>
    
            <div class="col-md-4">
              <div class="card mb-4 box-shadow"> 
                <a  href="marrtina.html">
                <img class="card-img-top" src="image/telepresence.png" alt="Marrtina">
                 </a>
                <div class="card-body">
</br></br></br></br></br>
                  <p class="card-text">Telepresenza.</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                      
                       <a class="btn btn-primary" href="navigation.php" role="button">TELEPRESENCE</a>
                    </div>
                    
                  </div>
                </div>
              </div>
            </div>
            
            <div class="col-md-4">
              <div class="card mb-4 box-shadow">
                <img class="card-img-top"  src="image/demo.png" alt="Card image cap">
                <div class="card-body">
                </br>
                  <p class="card-text">Demo Social</p>

                  <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                       
                      <a class="btn btn-primary" href="demorobotics.php" role="button">DEMO</a>
                    </div>
                    <small class="text-muted">9 mins</small>
                  </div>
                </div>
              </div>
            </div>


</div>

  


</body>

</html>


</body>

</html>
