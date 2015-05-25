
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
    var code = 'im_input';
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
    var value_output = Blockly.Python.valueToCode(block, 'output', Blockly.Python.ORDER_NONE);
    // TODO: Assemble Python into code variable.
    return Blockly.Python.multipleCodeToOutput(value_output,"im_output");
};

