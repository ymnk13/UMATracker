
Blockly.Blocks['im_circle_mask'] = {
    init: function() {
	this.setHelpUrl('http://www.example.com/');
	this.setColour(120);
	this.appendDummyInput()
            .appendField("Circle Center (X,Y) =(")
            .appendField(new Blockly.FieldTextInput("318"), "CenterX")
            .appendField(",")
            .appendField(new Blockly.FieldTextInput("230"), "CenterY")
            .appendField(")")
	this.appendDummyInput()
            .appendField("          Radius =")
            .appendField(new Blockly.FieldTextInput("183"), "Radius");
	this.setOutput(true);
	this.setTooltip('');
    }
};

Blockly.Python['im_circle_mask'] = function(block) {
    var value_im_circle_mask = Blockly.Python.valueToCode(block, 'im_circle_mask', Blockly.Python.ORDER_ATOMIC);
    var text_centerx = block.getFieldValue('CenterX');
    var text_centery = block.getFieldValue('CenterY');
    var text_radius = block.getFieldValue('Radius');    
    // TODO: Assemble Python into code variable.
    var code = [];
    code.push('width,height,dim = im_input.shape\r\n')
    code.push('im_mask = np.ones((width,height), dtype=np.uint8)\r\n')
    code.push('im_mask*=255\r\n')
    code.push('cv2.circle(im_mask,({0},{1}), radius = {2}, color = 0,thickness = -1)\r\n'.format(text_centerx,text_centery,text_radius));
    code.push('im_mask\n')
    //code.push('{0} = im_mask\r\n'.format(variable_im_variable))
    //code.push('{0} = im_mask\n'.format(variable_im_variable))
    var str_code =code.join("");
    // TODO: Change ORDER_NONE to the correct strength.
    return [str_code, Blockly.Python.ORDER_NONE];
};

Blockly.Blocks['im_rectangle_mask'] = {
    init: function() {
	this.setHelpUrl('http://www.example.com/');
	this.setColour(120);
	this.appendDummyInput()
            .appendField("Rectangle")
            .appendField("Top (X,Y) = (")
            .appendField(new Blockly.FieldTextInput("150"), "topX")
            .appendField(",")
            .appendField(new Blockly.FieldTextInput("150"), "topY")
            .appendField("),");
	this.appendDummyInput()
            .appendField("                 Bottom (X,Y) = ( ")
            .appendField(new Blockly.FieldTextInput("450"), "bottomX")
            .appendField(",")
            .appendField(new Blockly.FieldTextInput("500"), "bottomY")
            .appendField(")");
	this.setOutput(true);
	this.setTooltip('');
    }
};
Blockly.Python['im_rectangle_mask'] = function(block) {
    var text_topx = block.getFieldValue('topX');
    var text_topy = block.getFieldValue('topY');
    var text_bottomx = block.getFieldValue('bottomX');
    var text_bottomy = block.getFieldValue('bottomY');
    // TODO: Assemble Python into code variable.
    var code = [];
    code.push('width,height,dim = im_input.shape\r\n')
    code.push('im_mask = np.ones((width,height), dtype=np.uint8)\r\n')
    code.push('im_mask*=255\r\n')
    code.push('cv2.rectangle(im_mask,({0},{1}),({2},{3}) , color = 0,thickness = -1)\r\n'.format(text_topx,text_topy,text_bottomx,text_bottomy));
    code.push('im_mask\n')
    var str_code =code.join("\n");
    // TODO: Change ORDER_NONE to the correct strength.
    return [str_code, Blockly.Python.ORDER_NONE];
};
