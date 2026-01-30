class EyeController {
  constructor(elements = {}, eyeSize = '33.33vmin') {
    this._eyeSize = eyeSize;
    this._blinkTimeoutID = null;
    this._currentEmotion = 'normal'; // Track current emotion

    this.setElements(elements);
  }

  get leftEye() { return this._leftEye; }
  get rightEye() { return this._rightEye; }

  setElements({
    leftEye,
    rightEye,
    upperLeftEyelid,
    upperRightEyelid,
    lowerLeftEyelid,
    lowerRightEyelid,
    upperLeftMouthlid,
    upperRightMouthlid,
  } = {}) {
    this._leftEye = leftEye;
    this._rightEye = rightEye;
    this._upperLeftEyelid = upperLeftEyelid;
    this._upperRightEyelid = upperRightEyelid;
    this._lowerLeftEyelid = lowerLeftEyelid;
    this._lowerRightEyelid = lowerRightEyelid;
    this._upperLeftMouthlid = upperLeftMouthlid;
    this._upperRightMouthlid = upperRightMouthlid;
    return this;
  }

  _createKeyframes ({
    tgtTranYVal = 0,
    tgtRotVal = 0,
    enteredOffset = 1/3,
    exitingOffset = 2/3,
  } = {}) {
    return [
      {transform: `translateY(0px) rotate(0deg)`, offset: 0.0},
      {transform: `translateY(${tgtTranYVal}) rotate(${tgtRotVal})`, offset: enteredOffset},
      {transform: `translateY(${tgtTranYVal}) rotate(${tgtRotVal})`, offset: exitingOffset},
      {transform: `translateY(0px) rotate(0deg)`, offset: 1.0},
    ];
  }

  express({
    type = '',
    // level = 3,  // 1: min, 5: max
    duration = 1000,
    enterDuration = 75,
    exitDuration = 75,
  }) {
    if (!this._leftEye) {  // assumes all elements are always set together
      console.warn('Eye elements are not set; return;');
      return;
    }

    const options = {
      duration: duration,
    };
    
  }

  blink({
    duration = 150,  // in ms
  } = {}) {
    if (!this._leftEye) {  // assumes all elements are always set together
      console.warn('Eye elements are not set; return;');
      return;
    }

    [this._leftEye, this._rightEye].map((eye) => {
      eye.animate([
        {transform: 'rotateX(0deg)'},
        {transform: 'rotateX(90deg)'},
        {transform: 'rotateX(0deg)'},
      ], {
        duration,
        iterations: 1,
      });
    });
  }

  startBlinking({
    maxInterval = 5000
  } = {}) {
    if (this._blinkTimeoutID) {
      console.warn(`Already blinking with timeoutID=${this._blinkTimeoutID}; return;`);
      return;
    }
    const blinkRandomly = (timeout) => {
      this._blinkTimeoutID = setTimeout(() => {
        this.blink();
        blinkRandomly(Math.random() * maxInterval);
      }, timeout);
    }
    blinkRandomly(Math.random() * maxInterval);
  }

  stopBlinking() {
    clearTimeout(this._blinkTimeoutID);
    this._blinkTimeoutID = null;
  }
  
  normal() {
    this._currentEmotion = 'normal';
    document.getElementById("soprdx").src = "image/eyebrowdx1.gif"; 
    document.getElementById("soprsx").src = "image/eyebrowsx1.gif"; 
    document.getElementById("occhiodx").src = "image/eyedx.png"; 
    document.getElementById("occhiosx").src = "image/eyesx.png"; 	
    document.getElementById("bocca").src = "image/face01/Happy/mouthsmile.png"; 
    document.getElementById("naso").src = "image/nose.png"; 
    document.documentElement.style.setProperty("--eye-size", "16.00vmin");
    document.documentElement.style.setProperty("--eye-color", "white");
    document.documentElement.style.setProperty("--eye-top", "25%"); 
    document.documentElement.style.setProperty("--bulb-size", "33.33vmin");
    document.getElementById("lower-eyelid-left").style.opacity = "0";
    document.getElementById("lower-eyelid-right").style.opacity = "0";
    document.documentElement.style.setProperty("--lower-eyelid-color", "whitesmoke");
    document.documentElement.style.setProperty("--blush-opacity", "0.0");
    document.querySelector(".anger-marks").style.display = "none";
    document.querySelector(".thinking-light").style.display = "none";
    document.querySelector(".confused-spiral").style.display = "none";

    document.documentElement.style.setProperty("--eye-size", "16.00vmin");

  }	 
  
  happy() {
    this._currentEmotion = 'happy';
    document.getElementById("soprdx").src = "image/eyebrowdx5.gif"; 
    document.getElementById("soprsx").src = "image/eyebrowsx5.gif"; 
    document.getElementById("occhiodx").src = "image/face01/Happy/eyedx.png"; 
    document.getElementById("occhiosx").src = "image/face01/Happy/eyesx.png"; 	
    document.getElementById("bocca").src = "image/bocca.gif"; 
    document.getElementById("naso").src = "image/nose.png"; 
    document.documentElement.style.setProperty("--eye-size", "18.00vmin");
    document.documentElement.style.setProperty("--eye-color", "white");
    document.documentElement.style.setProperty("--eye-top", "25%"); 
    document.documentElement.style.setProperty("--bulb-size", "33.33vmin");
    document.getElementById("lower-eyelid-left").style.opacity = "0.5";
    document.getElementById("lower-eyelid-right").style.opacity = "0.5";
    document.documentElement.style.setProperty("--lower-eyelid-color", "whitesmoke");
    document.documentElement.style.setProperty("--blush-opacity", "0.3");
    document.querySelector(".anger-marks").style.display = "none";
    document.querySelector(".thinking-light").style.display = "none";
    document.querySelector(".confused-spiral").style.display = "none";
  }
	 
  angry() {
    this._currentEmotion = 'angry';
    document.getElementById("soprdx").src = "image/face01/Angry/eyebrowdxangry.png"; 
    document.getElementById("soprsx").src = "image/face01/Angry/eyebrowsxangry.png"; 
    document.getElementById("occhiodx").src = "image/face01/Angry/eyedxangry.png"; 
    document.getElementById("occhiosx").src = "image/face01/Angry/eyesxangry.png"; 	
    document.getElementById("bocca").src = "image/face01/Angry/mouthangry.png"; 
    document.getElementById("naso").src = "image/nose.png"; 
    document.documentElement.style.setProperty("--eye-size", "16.00vmin");
    document.documentElement.style.setProperty("--eye-color", "#b81414");
    document.documentElement.style.setProperty("--eye-top", "25%"); 
    document.documentElement.style.setProperty("--bulb-size", "33.33vmin");
    document.getElementById("lower-eyelid-left").style.opacity = "0.5";
    document.getElementById("lower-eyelid-right").style.opacity = "0.5";
    document.documentElement.style.setProperty("--lower-eyelid-color", "whitesmoke");
    document.documentElement.style.setProperty("--blush-opacity", "0.0");
    document.querySelector(".anger-marks").style.display = "block";
    document.querySelector(".thinking-light").style.display = "none";
    document.querySelector(".confused-spiral").style.display = "none";
  }

  sad() {
    this._currentEmotion = 'sad';
    document.getElementById("soprsx").src = "image/eyebrowsx3.gif"; 
    document.getElementById("soprdx").src = "image/eyebrowdx3.gif"; 
    document.getElementById("occhiodx").src = "image/face01/Sad/eyedxsad.png"; 
    document.getElementById("occhiosx").src = "image/face01/Sad/eyesxsad.png"; 	
    document.getElementById("bocca").src = "image/face03/sad/bocca.png"; 
    document.getElementById("naso").src = "image/nose.png";
    document.documentElement.style.setProperty("--eye-size", "10.00vmin");
    document.documentElement.style.setProperty("--eye-color", "white");
    document.documentElement.style.setProperty("--eye-top", "50%"); 
    document.documentElement.style.setProperty("--bulb-size", "33.33vmin");
    document.getElementById("lower-eyelid-left").style.opacity = "0.5";
    document.getElementById("lower-eyelid-right").style.opacity = "0.5";
    document.documentElement.style.setProperty("--lower-eyelid-color", "lightblue");
    document.documentElement.style.setProperty("--blush-opacity", "0.0");
    document.querySelector(".anger-marks").style.display = "none";
    document.querySelector(".thinking-light").style.display = "none";
    document.querySelector(".confused-spiral").style.display = "none";
  }

  focused() {
    this._currentEmotion = 'focused';
    document.getElementById("soprdx").src = "image/face01/Surprise/eyebrowdxsurprise.png"; 
    document.getElementById("soprsx").src = "image/eyebrowsx1.gif"; 
    document.getElementById("occhiodx").src = "image/eyedx.png"; 
    document.getElementById("occhiosx").src = "image/eyesx.png"; 	
    document.getElementById("bocca").src = "image/face03/normal/boccainv.png"; 
    document.getElementById("naso").src = "image/nose.png"; 
    document.documentElement.style.setProperty("--eye-size", "16.00vmin");
    document.documentElement.style.setProperty("--eye-color", "white");
    document.documentElement.style.setProperty("--bulb-size", "28.00vmin");
    document.documentElement.style.setProperty("--eye-top", "5%"); 
    document.getElementById("lower-eyelid-left").style.opacity = "0.5";
    document.getElementById("lower-eyelid-right").style.opacity = "0.5";
    document.documentElement.style.setProperty("--lower-eyelid-color", "whitesmoke");
    document.documentElement.style.setProperty("--blush-opacity", "0.0");
    document.querySelector(".anger-marks").style.display = "none";
    let light = document.querySelector(".thinking-light");
    light.style.display = "block"; 
    light.style.animation = "glow 1s infinite alternate";
    document.querySelector(".confused-spiral").style.display = "none";
  }
  
  surprise() {
    this._currentEmotion = 'surprise';
    document.getElementById("soprdx").src = "image/face01/Surprise/eyebrowdxsurprise.png"; 
    document.getElementById("soprsx").src = "image/face01/Surprise/eyebrowsxsurprise.png"; 
    document.getElementById("occhiodx").src = "image/face01/Surprise/eyedxsurprise.png"; 
    document.getElementById("occhiosx").src = "image/face01/Surprise/eyesxsurprise.png"; 	
    document.getElementById("bocca").src = "image/face01/Surprise/mouthsurprise.png"; 
    document.getElementById("naso").src = "image/nose.png";
    document.documentElement.style.setProperty("--eye-size", "16.00vmin");
    document.documentElement.style.setProperty("--eye-color", "white");
    document.documentElement.style.setProperty("--eye-top", "25%"); 
    document.documentElement.style.setProperty("--bulb-size", "33.33vmin");
    document.getElementById("lower-eyelid-left").style.opacity = "0";
    document.getElementById("lower-eyelid-right").style.opacity = "0";
    document.documentElement.style.setProperty("--lower-eyelid-color", "whitesmoke");
    document.documentElement.style.setProperty("--blush-opacity", "0.0");
    document.querySelector(".anger-marks").style.display = "none";
    document.querySelector(".thinking-light").style.display = "none";
    document.querySelector(".confused-spiral").style.display = "none";
    
  }
   
  embarrassed() {
    this._currentEmotion = 'embarrassed';
    document.getElementById("soprdx").src = "image/face01/Surprise/eyebrowdxsurprise.png"; 
    document.getElementById("soprsx").src = "image/face01/Surprise/eyebrowsxsurprise.png"; 
    document.getElementById("occhiodx").src = "image/eyedx.png"; 
    document.getElementById("occhiosx").src = "image/eyesx.png"; 	
    document.getElementById("bocca").src = "image/mouthclosed.png"; 
    document.getElementById("naso").src = "image/nose.png"; 
    document.documentElement.style.setProperty("--eye-size", "18.00vmin");
    document.documentElement.style.setProperty("--eye-color", "white");
    document.documentElement.style.setProperty("--eye-top", "12%"); 
    document.documentElement.style.setProperty("--bulb-size", "33.33vmin");
    document.getElementById("lower-eyelid-left").style.opacity = "0.5";
    document.getElementById("lower-eyelid-right").style.opacity = "0.5";
    document.documentElement.style.setProperty("--lower-eyelid-color", "whitesmoke");
    document.documentElement.style.setProperty("--blush-opacity", "0.9");	
    document.querySelector(".anger-marks").style.display = "none";
    document.querySelector(".thinking-light").style.display = "none";
    document.querySelector(".confused-spiral").style.display = "none";
  }

  confused() {
    this._currentEmotion = 'confused';
    document.getElementById("soprdx").src = "image/eyebrowdx.png"; 
    document.getElementById("soprsx").src = "image/face01/Surprise/eyebrowsxsurprise.png"; 
    document.getElementById("occhiodx").src = "image/eyedx.png"; 
    document.getElementById("occhiosx").src = "image/eyesx.png"; 	
    document.getElementById("bocca").src = "image/mouthclosed.png"; 
    document.getElementById("naso").src = "image/nose.png"; 
    document.documentElement.style.setProperty("--eye-size", "21.00vmin");
    document.documentElement.style.setProperty("--eye-color", "#d7d7d7");
    document.documentElement.style.setProperty("--bulb-size", "35.33vmin");
    document.documentElement.style.setProperty("--eye-top", "25%"); 
    document.getElementById("lower-eyelid-left").style.opacity = "0.2";
    document.getElementById("lower-eyelid-right").style.opacity = "0.2";
    document.documentElement.style.setProperty("--lower-eyelid-color", "whitesmoke");
    document.documentElement.style.setProperty("--blush-opacity", "0.0");
    document.querySelector(".anger-marks").style.display = "none";
    document.querySelector(".thinking-light").style.display = "none";
    document.querySelector(".confused-spiral").style.display = "block";
  }
  
  closeEyes() {
    if (!this._leftEye) {  // assumes all elements are always set together
      console.warn('Eye elements are not set; return;');
      return;
    }

    document.getElementById("occhiodx").src = "image/eyedx_closed.png"; 
    document.getElementById("occhiosx").src = "image/eyesx_closed.png"; 	
	document.getElementById("soprdx").src = "image/face01/Happy/eyebrowdx.png"; 
    document.getElementById("soprsx").src = "image/face01/Happy/eyebrowsx.png"; 
    document.getElementById("bocca").src = "image/face01/Sad/mouthclosed.png"; 

    document.documentElement.style.setProperty("--eye-size", "0.00vmin");
    /*
    const eyeElem = document.querySelectorAll('.eye');
    eyeElem.forEach(element => {
      element.style.width = '0px';
    });*/
  }

  speak(emotion = 'normal') {
    // Apply the specified emotion first to restore all its properties
    if (emotion === "normal") this.normal();
    else if (emotion === "happy") this.happy();
    else if (emotion === "surprise") this.surprise();
    else if (emotion === "angry") this.angry();
    else if (emotion === "sad") this.sad();
    else if (emotion === "focused") this.focused();
    else if (emotion === "confused") this.confused();
    else if (emotion === "embarrassed") this.embarrassed();
    else this.normal();
    
    // Then change only the mouth and nose to talking
    document.getElementById("naso").src = "image/nosetalkmarrtina1.gif"; 
    // Use a different mouth accoring to the emotion
    if (emotion === "surprise" || emotion === "angry" || emotion === "embarassed")
    {
      document.getElementById("bocca").src = "image/mouthtalkmarrtina1.gif"; 
    }
    else{
      document.getElementById("bocca").src = "image/mouthtalkmarrtina2.gif"; 
    }
      
  }



  sings() {
    document.getElementById("bocca").src = "image/boccachecanta.gif"; 
    document.getElementById("naso").src = "image/nosetalkmarrtina1.gif"; 
    document.documentElement.style.setProperty("--eye-size", "16.00vmin");
    document.documentElement.style.setProperty("--eye-color", "white");
    document.documentElement.style.setProperty("--eye-top", "25%"); 
    document.documentElement.style.setProperty("--bulb-size", "33.33vmin");
    document.getElementById("lower-eyelid-left").style.opacity = "0";
    document.getElementById("lower-eyelid-right").style.opacity = "0";
    document.documentElement.style.setProperty("--lower-eyelid-color", "whitesmoke");
    document.documentElement.style.setProperty("--blush-opacity", "0.0");
    document.querySelector(".anger-marks").style.display = "none";
    document.querySelector(".thinking-light").style.display = "none";
    document.querySelector(".confused-spiral").style.display = "none";
  }  


  setEyePosition(eyeElem, x, y, isRight = false) {
    if (!eyeElem) {  // assumes all elements are always set together
      console.warn('Invalid inputs ', eyeElem, x, y, '; retuning');
      return;
    }

    if (!!x) {
      if (!isRight) {
        eyeElem.style.left = `calc(${this._eyeSize} / 3 * 2 * ${x})`;
      } else {
        eyeElem.style.right = `calc(${this._eyeSize} / 3 * 2 * ${1-x})`;
      }
    }
    if (!!y) {
      eyeElem.style.bottom = `calc(${this._eyeSize} / 3 * 2 * ${1-y})`;
    }
  }
}

const eyes = new EyeController({
  leftEye: document.querySelector('.left.bulb'),
  rightEye: document.querySelector('.right.bulb'),
  upperLeftEyelid: document.querySelector('.left .eyelid.upper'),
  upperRightEyelid: document.querySelector('.right .eyelid.upper'),
  lowerLeftEyelid: document.querySelector('.left .eyelid.lower'),
  lowerRightEyelid: document.querySelector('.right .eyelid.lower'),
  upperLeftMouthlid: document.querySelector('.mouthid.upper'),
  lowerLeftMouthlid: document.querySelector('.mouthid.lower'),
  
});
