// Python code generation

Blockly.Python['begin'] = function(block) {
  var code = 'begin()\n';
  return code;
};

Blockly.Python['end'] = function(block) {
  var code = 'end()\n';
  return code;
};

Blockly.Python['forward'] = function(block) {
  var value_steps = Blockly.Python.valueToCode(block, 'steps', Blockly.Python.ORDER_ATOMIC);
  var code = 'forward('+value_steps+')\n';
  return code;
};

Blockly.Python['backward'] = function(block) {
  var value_steps = Blockly.Python.valueToCode(block, 'steps', Blockly.Python.ORDER_ATOMIC);
  var code = 'backward('+value_steps+')\n';
  return code;
};

Blockly.Python['left'] = function(block) {
  var value_steps = Blockly.Python.valueToCode(block, 'steps', Blockly.Python.ORDER_ATOMIC);
  var code = 'left('+value_steps+')\n';
  return code;
};

Blockly.Python['right'] = function(block) {
  var value_steps = Blockly.Python.valueToCode(block, 'steps', Blockly.Python.ORDER_ATOMIC);
  var code = 'right('+value_steps+')\n';
  return code;
};

Blockly.Python['wait'] = function(block) {
  var value_seconds = Blockly.Python.valueToCode(block, 'seconds', Blockly.Python.ORDER_ATOMIC);
  var code = 'wait('+value_seconds+')\n';
  return code;
};

Blockly.Python['turn'] = function(block) {
  var value_deg = Blockly.Python.valueToCode(block, 'degrees', Blockly.Python.ORDER_ATOMIC);
  var code = 'turn('+value_deg+')\n';
  return code;
};

Blockly.Python['setSpeed'] = function(block) {
  var value_tv = Blockly.Python.valueToCode(block, 'tv', Blockly.Python.ORDER_ATOMIC);
  var value_rv = Blockly.Python.valueToCode(block, 'rv', Blockly.Python.ORDER_ATOMIC);
  var value_time = Blockly.Python.valueToCode(block, 'time', Blockly.Python.ORDER_ATOMIC);
  var code = 'setSpeed('+value_tv+','+value_rv+','+value_time+',False)\n';
  return code;
};


Blockly.Python['get_pose'] = function(block) {
  var code = 'get_robot_pose()';
  return [code, Blockly.Python.ORDER_NONE];
};



Blockly.Python['obstacle_distance'] = function(block) {
  var dropdown_direction = block.getFieldValue('direction');
  var v=0
  if (dropdown_direction == "OPTIONFRONT") { v = 0; }
  else if (dropdown_direction == "OPTIONLEFT") { v = 90; }
  else if (dropdown_direction == "OPTIONRIGHT") { v = -90; }
  else if (dropdown_direction == "OPTIONBACK") { v = 180; }
  var code = 'obstacle_distance('+v+')';
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['distance'] = function(block) {
  var value_p1 = Blockly.Python.valueToCode(block, 'P1', Blockly.Python.ORDER_ATOMIC);
  var value_p2 = Blockly.Python.valueToCode(block, 'P2', Blockly.Python.ORDER_ATOMIC);
  var code = 'distance('+value_p1+','+value_p2+')';
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['random'] = function(block) {
  Blockly.Python.definitions_.import_random="import random";
  var value_1 = Blockly.Python.valueToCode(block, 'min', Blockly.Python.ORDER_ATOMIC);
  var value_2 = Blockly.Python.valueToCode(block, 'max', Blockly.Python.ORDER_ATOMIC);
  var code = 'random.randint('+value_1+','+value_2+')';
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['marrtino_ok'] = function(block) {
  var code = 'marrtino_ok()';
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['display'] = function(block) {
  var value_text = Blockly.Python.valueToCode(block, 'text', Blockly.Python.ORDER_ATOMIC);
  var code = 'display('+value_text+')\n';
  return code;
};


Blockly.Python['say'] = function(block) {
  var value_text = Blockly.Python.valueToCode(block, 'text', Blockly.Python.ORDER_ATOMIC);
  var value_lang = Blockly.Python.valueToCode(block, 'lang', Blockly.Python.ORDER_ATOMIC);
  var code = 'say('+value_text+','+value_lang+')\n';
  return code;
};

Blockly.Python['sound'] = function(block) {
  var value_name = Blockly.Python.valueToCode(block, 'name', Blockly.Python.ORDER_ATOMIC);
  var code = 'sound('+value_name+')\n';
  return code;
};


Blockly.Python['face'] = function(block) {
  var dropdown_emotion = block.getFieldValue('EMOTION');
  // TODO: Assemble Python into code variable.
  var code = 'emotion("'+dropdown_emotion+'")\n';
  return code;
}

Blockly.Python['status'] = function(block) {
  var dropdown_status = block.getFieldValue('STATUS');
  // TODO: Assemble Python into code variable.
  var code = 'emotion("'+dropdown_status+'")\n';
  return code;
}


Blockly.Python['head_position'] = function(block) {
  var dropdown_position = block.getFieldValue('HEAD_POSITION');
  // TODO: Assemble Python into code variable.
  var code = 'head_position("'+dropdown_position+'")\n';
  return code;
}

Blockly.Python['get_stt'] = function(block) {
  var code = 'get_stt()';
  return [code, Blockly.Python.ORDER_NONE];
};


Blockly.Python['get_nro_of_face'] = function(block) {
  var code = 'get_nro_of_face()';
  return [code, Blockly.Python.ORDER_NONE];
};



Blockly.Python['pan'] = function(block) {
  var value_sign = block.getFieldValue('Sign');
  var value_steps = Blockly.Python.valueToCode(block, 'steps', Blockly.Python.ORDER_ATOMIC);
  if ( value_sign == '-') { 
    value_steps = -value_steps;
  }
  var value_pos = (value_steps); // / 100) -0.5;
  var code = 'pan('+value_pos+')\n';
  return code;
};

Blockly.Python['tilt'] = function(block) {
  var value_sign = block.getFieldValue('Sign');
  var value_steps = Blockly.Python.valueToCode(block, 'steps', Blockly.Python.ORDER_ATOMIC);
  if ( value_sign == '-') { 
    value_steps = -value_steps;
  }
  var value_pos = (value_steps / 100) -0.5 * -1;
  var code = 'tilt('+value_pos+')\n';
  return code;
};

// 150 Rappresenza 0 
Blockly.Python['spalla_flessione_dx'] = function(block) {
  var value_sign = block.getFieldValue('Sign');
  var value_steps = Blockly.Python.valueToCode(block, 'steps', Blockly.Python.ORDER_ATOMIC);
  if ( value_sign == '-') { 
    value_steps = -value_steps;
  }
  var value_pos = (((150 + parseInt(value_steps))* 3.14 )/ 180) ; 
  var code = 'spalla_flessione_dx('+value_pos+')\n';
  return code;
};

Blockly.Python['spalla_flessione_sx'] = function(block) {
  var value_sign = block.getFieldValue('Sign');
  var value_steps = Blockly.Python.valueToCode(block, 'steps', Blockly.Python.ORDER_ATOMIC);
  if ( value_sign == '+') { 
    value_steps = -value_steps;
  }
  var value_pos = (((150 + parseInt(value_steps))* 3.14 )/ 180) ;
  var code = 'spalla_flessione_sx('+value_pos+')\n';
  return code;
};


Blockly.Python['spalla_rotazione_dx'] = function(block) {
  var value_sign = block.getFieldValue('Sign');
  var value_steps = Blockly.Python.valueToCode(block, 'steps', Blockly.Python.ORDER_ATOMIC);
  if ( value_sign == '+') { 
    value_steps = -value_steps;
  }
  var value_pos = (((150 + parseInt(value_steps))* 3.14 )/ 180) ;
  var code = 'spalla_rotazione_dx('+value_pos+')\n';
  return code;
};


Blockly.Python['spalla_rotazione_sx'] = function(block) {
  var value_sign = block.getFieldValue('Sign');
  var value_steps = Blockly.Python.valueToCode(block, 'steps', Blockly.Python.ORDER_ATOMIC);
  if ( value_sign == '-') { 
    value_steps = -value_steps;
  }
  var value_pos = (((150 + parseInt(value_steps))* 3.14 )/ 180) ;
  var code = 'spalla_rotazione_sx('+value_pos+')\n';
  return code;
};
Blockly.Python['gomito_dx'] = function(block) {
  var value_sign = block.getFieldValue('Sign');
  var value_steps = Blockly.Python.valueToCode(block, 'steps', Blockly.Python.ORDER_ATOMIC);
  if ( value_sign == '+') { 
    //if ( parseInt(value_steps) > 30 ) { value_steps = 30  }
    value_steps = -value_steps;
  }
  var value_pos = (((150 + parseInt(value_steps))* 3.14 )/ 180) ;
  var code = 'gomito_dx('+value_pos+')\n';
  return code;
};


Blockly.Python['gomito_sx'] = function(block) {
  var value_sign = block.getFieldValue('Sign');
  var value_steps = Blockly.Python.valueToCode(block, 'steps', Blockly.Python.ORDER_ATOMIC);
  if ( value_sign == '-') { 
    if ( value_steps > 30 )
      //if ( parseInt(value_steps) > 30 ) { value_steps = 30  }
      value_steps = -value_steps;

  }
  var value_pos = (((150 + parseInt(value_steps))* 3.14 )/ 180) ;
  var code = 'gomito_sx('+value_pos+')\n';
  return code;
};




Blockly.Python['run_python'] = function(block) {
  var value_text = Blockly.Python.valueToCode(block, 'text', Blockly.Python.ORDER_ATOMIC);
  var code = value_text;
  code = code.substring(1, code.length - 1) +'\n';
  return code;

};


Blockly.Python['user_say'] = function(block) {
  var code = 'user_say()';
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['wait_user_speaking'] = function(block) {
  var value_seconds = Blockly.Python.valueToCode(block, 'seconds', Blockly.Python.ORDER_ATOMIC);
  var code = 'wait_user_speaking('+value_seconds+') # second \n';
  return code;
};

Blockly.Python['logic_boolean'] = function(block) {
  var value_text = Blockly.Python.valueToCode(block, 'text', Blockly.Python.ORDER_ATOMIC);
   
  var code = value_text;
  code = code.substring(1, code.length - 1) +'\n';
 
  
  return code;

};

Blockly.Python['tag_trigger'] = function(block) {
  var code = 'tagTrigger()';
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python['tag_id'] = function(block) {
  var code = 'tagID()';
  return [code, Blockly.Python.ORDER_NONE];
};
Blockly.Python['tag_distance'] = function(block) {
  var code = 'tagDistance()';
  return [code, Blockly.Python.ORDER_NONE];
};
Blockly.Python['tag_angle'] = function(block) {
  var code = 'tagAngle()';
  return [code, Blockly.Python.ORDER_NONE];
};
Blockly.Python['get_image'] = function(block) {
  var code = 'getImage()';
  return [code, Blockly.Python.ORDER_NONE];
};
Blockly.Python['face_detection'] = function(block) {
  var value_img = Blockly.Python.valueToCode(block, 'img', Blockly.Python.ORDER_ATOMIC);
  var code = 'faceDetection('+value_img+')';
  return [code, Blockly.Python.ORDER_NONE];
};