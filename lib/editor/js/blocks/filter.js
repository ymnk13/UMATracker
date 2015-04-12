Blockly.Blocks['img_gray_bgrtogray'] = {
	init: function() {
		this.setHelpUrl('http://www.example.com/');
		this.appendValueInput("img")
			.setCheck("Image_BGR")
			.setAlign(Blockly.ALIGN_RIGHT)
			.appendField("BGRToGray");
		this.setOutput(true, "Image_GRAY");
		this.setTooltip('');
	}
};

Blockly.Python['img_gray_bgrtogray'] = function(block) {
	var value_img = Blockly.Python.valueToCode(block, 'img', Blockly.Python.ORDER_ATOMIC);
	// TODO: Assemble Python into code variable.
    var code = 'cv2.cvtColor({0},CV_BGR2GRAY)'.format(value_img);
    var code = 'cv2.cvtColor({0},cv2.COLOR_BGR2GRAY)\n'.format(value_img);

	// TODO: Change ORDER_NONE to the correct strength.
	return [code, Blockly.Python.ORDER_NONE];
};


Blockly.Blocks['im_threshold'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.appendValueInput("im_threshold")
        .appendField("Threshold :")
        .appendField(new Blockly.FieldTextInput("100"), "threshold");
    this.setOutput(true);
    this.setTooltip('');
  }
};

Blockly.Python['im_threshold'] = function(block) {
  var value_im_threshold = Blockly.Python.valueToCode(block, 'im_threshold', Blockly.Python.ORDER_ATOMIC);
  var text_threshold = block.getFieldValue('threshold');
  // TODO: Assemble Python into code variable.
  var code = 'cv2.threshold({0},{1},255,cv2.THRESH_BINARY)[1]'.format(value_im_threshold,text_threshold);
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};
  
