Blockly.Blocks['img_gray_absdiff'] = {
	init: function() {
		this.setHelpUrl('http://www.example.com/');
		this.appendValueInput("img1")
			.setCheck("Image_GRAY")
			.appendField("img1").setAlign(Blockly.ALIGN_RIGHT);
		this.appendDummyInput()
			.appendField('absdiff')
			.setAlign(Blockly.ALIGN_CENTER)
			this.appendValueInput("img2")
			.setCheck("Image_GRAY")
			.appendField("img2").setAlign(Blockly.ALIGN_RIGHT);
		this.setOutput(true, "Image_GRAY");
		this.setTooltip('');
	}
};
Blockly.Python['img_gray_absdiff'] = function(block) {
	var value_img1 = Blockly.Python.valueToCode(block, 'img1', Blockly.Python.ORDER_ATOMIC);
	var value_img2 = Blockly.Python.valueToCode(block, 'img2', Blockly.Python.ORDER_ATOMIC);
	// TODO: Assemble Python into code variable.
	var code = 'cv2.absdiff({0},{1})'.format(value_img1,value_img2);
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
	var value_img1 = Blockly.Python.valueToCode(block, 'img1', Blockly.Python.ORDER_ATOMIC);
	var value_img2 = Blockly.Python.valueToCode(block, 'img2', Blockly.Python.ORDER_ATOMIC);
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
    var value_im_origin = Blockly.Python.valueToCode(block, 'im_origin', Blockly.Python.ORDER_ATOMIC);
    var value_im_mask = Blockly.Python.valueToCode(block, 'im_mask', Blockly.Python.ORDER_ATOMIC);
    // TODO: Assemble Python into code variable.
    var originCodes = Blockly.Python.multipleCodeSplit(value_im_origin);
    var maskCodes = Blockly.Python.multipleCodeSplit(value_im_mask);
    var code = []
    value_im_origin = originCodes[1].replace(/[\n\r]/g,"")
    if(originCodes[0] == ''){
	
    }else{
	code.push(originCodes[0])
    }
    value_im_mask = maskCodes[1].replace(/[\n\r]/g,"")
    if(maskCodes[0] == ''){
	
    }else{
	code.push(maskCodes[0])
    }
    code.push('cv2.max({0},{1})'.format(value_im_origin,value_im_mask))
    var codeStr = code.join('\n')
    // TODO: Change ORDER_NONE to the correct strength.
    return [codeStr, Blockly.Python.ORDER_NONE];
};

