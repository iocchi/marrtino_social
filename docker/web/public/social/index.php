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
            <a href="https://www.artigianitecnologici.it">
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
                  <p class="card-text">BRINGUP</p>
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
                <img class="card-img-top" src="image/MarrtinoInterface.jpg" alt="Marrtina">
                 </a>
                <div class="card-body">
                  <p class="card-text">Social interface Marrtino Robot.</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                      
                       <a class="btn btn-primary" href="facerobot.php" role="button">Social Interface</a>
                    </div>
                    
                  </div>
                </div>
              </div>
            </div>
            <h3> </h3>
    
            <div class="col-md-4">
              <div class="card mb-4 box-shadow"> 
                <a  href="../chess">
                <img class="card-img-top" src="image/chess.jpg" alt="Scacchi">
                 </a>
                <div class="card-body">
                  <p class="card-text">Chess.</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                      
                       <a class="btn btn-primary" href="../chess" role="button">Chess</a>
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
                <img class="card-img-top" src="image/MarrtinoInterface.jpg" alt="Marrtina">
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
                <img class="card-img-top" src="image/face01/MarrtinaIcona.jpg" alt="Marrtina">
                 </a>
                <div class="card-body">
                  <p class="card-text">Telepresenza.</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                      
                       <a class="btn btn-primary" href="4WD_offline.html" role="button">telepresenza</a>
                    </div>
                    
                  </div>
                </div>
              </div>
            </div>
            
            <div class="col-md-4">
              <div class="card mb-4 box-shadow">
                <img class="card-img-top" data-src="holder.js/100px225?theme=thumb&bg=55595c&fg=eceeef&text=Thumbnail" alt="Card image cap">
                <div class="card-body">
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
