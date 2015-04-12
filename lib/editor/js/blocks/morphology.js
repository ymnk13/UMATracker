Blockly.Blocks['cv_erosion'] = {
    init: function() {
	this.setHelpUrl('http://www.example.com/');
	this.appendValueInput("NAME")
            .appendField("Erosion: Kernel =")
            .appendField(new Blockly.FieldTextInput("5"), "SIZE");
	this.setOutput(true);
	this.setTooltip('');
    }
};

Blockly.Python['cv_erosion'] = function(block) {
    var value_name = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var text_size = block.getFieldValue('SIZE');
    // TODO: Assemble Python into code variable.
    var code = [];
    code.push('kernel = np.ones(({0},{0}),np.uint8)\n'.format(text_size))
    code.push('cv2.erode({0},kernel,iterations = 1)\n'.format(value_name))
    var str_code =code.join("\n");
    // TODO: Change ORDER_NONE to the correct strength.
    return [str_code, Blockly.Python.ORDER_MEMBER];
};

Blockly.Blocks['cv_dilation'] = {
    init: function() {
	this.setHelpUrl('http://www.example.com/');
	this.appendValueInput("NAME")
            .appendField("Dilation: Kernel =")
            .appendField(new Blockly.FieldTextInput("5"), "SIZE");
	this.setOutput(true);
	this.setTooltip('');
    }
};

Blockly.Python['cv_dilation'] = function(block) {
    var value_name = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var text_size = block.getFieldValue('SIZE');
    // TODO: Assemble Python into code variable.
    var code = [];
    code.push('kernel = np.ones(({0},{0}),np.uint8)\n'.format(text_size))
    code.push('cv2.dilate({0},kernel,iterations = 1)\n'.format(value_name))
    var str_code =code.join("\n");
    // TODO: Change ORDER_NONE to the correct strength.
    return [str_code, Blockly.Python.ORDER_MEMBER];
};


Blockly.Blocks['cv_opening'] = {
    init: function() {
	this.setHelpUrl('http://www.example.com/');
	this.appendValueInput("NAME")
            .appendField("Opening: Kernel =")
            .appendField(new Blockly.FieldTextInput("5"), "SIZE");
	this.setOutput(true);
	this.setTooltip('');
    }
};

Blockly.Python['cv_opening'] = function(block) {
    var value_name = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var text_size = block.getFieldValue('SIZE');
    // TODO: Assemble Python into code variable.
    var code = [];
    code.push('kernel = np.ones(({0},{0}),np.uint8)\n'.format(text_size))
    code.push('cv2.morphologyEx({0},cv2.MORPH_OPEN,kernel)\n'.format(value_name))
    var str_code =code.join("\n");
    // TODO: Change ORDER_NONE to the correct strength.
    return [str_code, Blockly.Python.ORDER_MEMBER];
};



Blockly.Blocks['cv_closing'] = {
    init: function() {
	this.setHelpUrl('http://www.example.com/');
	this.appendValueInput("NAME")
            .appendField("Closing: Kernel =")
            .appendField(new Blockly.FieldTextInput("5"), "SIZE");
	this.setOutput(true);
	this.setTooltip('');
    }
};

Blockly.Python['cv_closing'] = function(block) {
    var value_name = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var text_size = block.getFieldValue('SIZE');
    // TODO: Assemble Python into code variable.
    var code = [];
    code.push('kernel = np.ones(({0},{0}),np.uint8)\n'.format(text_size))
    code.push('cv2.morphologyEx({0},cv2.MORPH_CLOSE,kernel)\n'.format(value_name))
    var str_code =code.join("\n");
    // TODO: Change ORDER_NONE to the correct strength.
    return [str_code, Blockly.Python.ORDER_MEMBER];
};


