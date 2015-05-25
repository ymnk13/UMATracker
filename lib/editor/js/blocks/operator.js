Blockly.Blocks['img_gray_absdiff'] = {
    init: function() {
	this.setHelpUrl('http://www.example.com/');
	this.appendValueInput("img1")
	    .setCheck("Image_GRAY")
	    .appendField("A").setAlign(Blockly.ALIGN_RIGHT);
	this.appendDummyInput()
	    .appendField('    | A-B |')
	    .setAlign(Blockly.ALIGN_CENTER)
	this.appendValueInput("img2")
	    .setCheck("Image_GRAY")
	    .appendField("B").setAlign(Blockly.ALIGN_RIGHT);
	this.setOutput(true, "Image_GRAY");
	this.setTooltip('');
    }
};
Blockly.Python['img_gray_absdiff'] = function(block) {
    var value_img1 = Blockly.Python.valueToCode(block, 'img1', Blockly.Python.ORDER_NONE);
    var value_img2 = Blockly.Python.valueToCode(block, 'img2', Blockly.Python.ORDER_NONE);
    // TODO: Assemble Python into code variable.
    var code = Blockly.Python.joinCodesToOperator(value_img1,value_img2,'cv2.absdiff({0},{1})')
    // TODO: Change ORDER_NONE to the correct strength.
    return [code, Blockly.Python.ORDER_NONE];
};


Blockly.Blocks['img_bgr_absdiff'] = {
    init: function() {
	this.setColour(0);
	this.setHelpUrl('http://www.example.com/');
	this.appendValueInput("img1")
	    .setCheck("Image_BGR")
	    .appendField("img1").setAlign(Blockly.ALIGN_RIGHT);
	this.appendDummyInput()
	    .appendField('absdiff')
	    .setAlign(Blockly.ALIGN_CENTER)
	this.appendValueInput("img2")
	    .setCheck("Image_BGR")
	    .appendField("img2").setAlign(Blockly.ALIGN_RIGHT);
	this.setOutput(true, "Image_BGR");
	this.setTooltip('');
    }
};
Blockly.Python['img_bgr_absdiff'] = function(block) {
    var value_img1 = Blockly.Python.valueToCode(block, 'img1', Blockly.Python.ORDER_NONE);
    var value_img2 = Blockly.Python.valueToCode(block, 'img2', Blockly.Python.ORDER_NONE);
    // TODO: Assemble Python into code variable.
    var code = 'cv2.absdiff({0},{1})'.format(value_img1,value_img2);
    // TODO: Change ORDER_NONE to the correct strength.
    return [code, Blockly.Python.ORDER_NONE];
};


Blockly.Blocks['im_mask'] = {
    init: function() {
	this.setHelpUrl('http://www.example.com/');
	this.setColour(330);
	this.appendValueInput("im_origin")
	    .appendField("origin image");
	this.appendValueInput("im_mask")
	    .appendField("mask image");
	this.setOutput(true);
	this.setTooltip('');
    }
};

Blockly.Python['im_mask'] = function(block) {
    var value_im_origin = Blockly.Python.valueToCode(block, 'im_origin', Blockly.Python.ORDER_NONE);
    var value_im_mask = Blockly.Python.valueToCode(block, 'im_mask', Blockly.Python.ORDER_NONE);
    // TODO: Assemble Python into code variable.
    var code = Blockly.Python.joinCodesToOperator(value_im_origin,value_im_mask,'cv2.max({0},{1})')
    // TODO: Change ORDER_NONE to the correct strength.
    return [code, Blockly.Python.ORDER_NONE];
};


Blockly.Blocks['operator_and'] = {
    init: function() {
	this.setHelpUrl('http://www.example.com/');
	this.setColour(230);
	this.appendValueInput("inputA")
            .appendField("        A");
	this.appendDummyInput()
            .appendField("  A and B");
	this.appendValueInput("inputB")
            .appendField("        B");
	this.setOutput(true);
	this.setTooltip('');
    }
};

Blockly.Python['operator_and'] = function(block) {
    var value_inputa = Blockly.Python.valueToCode(block, 'inputA', Blockly.Python.ORDER_NONE);
    var value_inputb = Blockly.Python.valueToCode(block, 'inputB', Blockly.Python.ORDER_NONE);
    // TODO: Assemble Python into code variable.
    var code = Blockly.Python.joinCodesToOperator(value_inputa,value_inputb,'cv2.bitwise_and({0},{1})')
    // TODO: Change ORDER_NONE to the correct strength.
    return [code, Blockly.Python.ORDER_NONE];
};


Blockly.Blocks['operator_or'] = {
    init: function() {
	this.setHelpUrl('http://www.example.com/');
	this.setColour(230);
	this.appendValueInput("inputA")
            .appendField("        A");
	this.appendDummyInput()
            .appendField("  A or B");
	this.appendValueInput("inputB")
            .appendField("        B");
	this.setOutput(true);
	this.setTooltip('');
    }
};

Blockly.Python['operator_or'] = function(block) {
    var value_inputa = Blockly.Python.valueToCode(block, 'inputA', Blockly.Python.ORDER_NONE);
    var value_inputb = Blockly.Python.valueToCode(block, 'inputB', Blockly.Python.ORDER_NONE);
    // TODO: Assemble Python into code variable.
    var code = Blockly.Python.joinCodesToOperator(value_inputa,value_inputb,'cv2.bitwise_or({0},{1})')
    // TODO: Change ORDER_NONE to the correct strength.
    return [code, Blockly.Python.ORDER_NONE];
};
