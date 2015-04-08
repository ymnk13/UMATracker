if (!String.prototype.format) {
	String.prototype.format = function() {
		var args = arguments;
		return this.replace(/{(\d+)}/g, function(match, number) {
			return typeof args[number] != 'undefined'
				? args[number]
				: match
				;
		});
	};
}

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

Blockly.Blocks['input'] = {
	init: function() {
		this.setColour(0);
		this.setHelpUrl('http://www.example.com/');
		this.appendDummyInput()
			.appendField("input");
		this.setInputsInline(true);
		this.setOutput(true, "Image_BGR");
		this.setTooltip('');
	}
};
Blockly.Python['input'] = function(block) {
	// TODO: Assemble Python into code variable.
	var code = 'input';
	// TODO: Change ORDER_NONE to the correct strength.
	return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Blocks['background'] = {
	init: function() {
		this.setColour(0);
		this.setHelpUrl('http://www.example.com/');
		this.appendDummyInput()
			.appendField("background");
		this.setInputsInline(true);
		this.setOutput(true, "Image_BGR");
		this.setTooltip('');
	}
};
Blockly.Python['background'] = function(block) {
	// TODO: Assemble Python into code variable.
	var code = 'background';
	// TODO: Change ORDER_NONE to the correct strength.
	return [code, Blockly.Python.ORDER_NONE];
};

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
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};


Blockly.Blocks['output'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.appendValueInput("output")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("output");
    this.setInputsInline(true);
    this.setPreviousStatement(true);
    this.setTooltip('');
  }
};

Blockly.Python['output'] = function(block) {
  var value_output = Blockly.Python.valueToCode(block, 'output', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = 'output = {0}'.format(value_output);
  return code;
};

Blockly.inject(document.getElementById('blocklyDiv'),
		{toolbox: document.getElementById('toolbox')});
Blockly.Xml.domToWorkspace(Blockly.mainWorkspace,
		document.getElementById('startBlocks'));

function showCode() {
	// Generate JavaScript code and display it.
	Blockly.Python.INFINITE_LOOP_TRAP = null;
	var code = Blockly.Python.workspaceToCode();
	alert(code);
}
