Blockly.Blocks['im_circle_mask'] = {
    init: function() {
        this.setHelpUrl('http://www.example.com/');
        this.setColour(120);
        this.appendDummyInput()
            .appendField("Circle Center (X,Y) =(")
            .appendField(new Blockly.FieldTextInput("0.5"), "CenterX")
            .appendField(",")
            .appendField(new Blockly.FieldTextInput("0.5"), "CenterY")
            .appendField(")");
        this.appendDummyInput()
            .appendField("          Radius =")
            .appendField(new Blockly.FieldTextInput("0.3"), "Radius");
        this.setOutput(true);
        this.setTooltip('');
    }
};

Blockly.Python['im_circle_mask'] = function(block) {
    var value_im_circle_mask = Blockly.Python.valueToCode(block, 'im_circle_mask', Blockly.Python.ORDER_NONE);
    var text_centerx = block.getFieldValue('CenterX');
    var text_centery = block.getFieldValue('CenterY');
    var text_radius = block.getFieldValue('Radius');
    // TODO: Assemble Python into code variable.
    var code = [];
    var im_mask_name = "self.im_mask_{0}".format(orgFunc.randStr());
    code.push('#self.height, self.width, self.dim = {input}.shape\r\n');
    code.push('#{0} = np.zeros((self.height, self.width), dtype=np.uint8)\r\n'.format(im_mask_name));
    // code.push('{0}*=255\r\n'.format(im_mask_name));
    code.push('#cv2.circle({3}, (int({0}*self.width), int({1}*self.height)), radius = int({2}*self.width/2), color = 255,thickness = -1)\r\n'.format(text_centerx,text_centery,text_radius,im_mask_name));
    code.push('{0}\n'.format(im_mask_name));
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
            .appendField(new Blockly.FieldTextInput("0.1"), "topX")
            .appendField(",")
            .appendField(new Blockly.FieldTextInput("0.1"), "topY")
            .appendField("),");
        this.appendDummyInput()
            .appendField("                 Bottom (X,Y) = ( ")
            .appendField(new Blockly.FieldTextInput("0.9"), "bottomX")
            .appendField(",")
            .appendField(new Blockly.FieldTextInput("0.9"), "bottomY")
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
    var im_mask_name = "self.im_mask_{0}".format(orgFunc.randStr());
    var code = [];
    code.push('#self.height, self.width, self.dim = {input}.shape\r\n');
    code.push('#{0} = np.zeros((self.height, self.width), dtype=np.uint8)\r\n'.format(im_mask_name));
    // code.push('{0}*=255\r\n'.format(im_mask_name));
    code.push('#cv2.rectangle({4}, (int({0}*self.width), int({1}*self.height)), (int({2}*self.width), int({3}*self.height)) , color = 255,thickness = -1)\r\n'.format(text_topx,text_topy,text_bottomx,text_bottomy,im_mask_name));
    code.push('{0}\n'.format(im_mask_name));
    var str_code =code.join("\n");
    // TODO: Change ORDER_NONE to the correct strength.
    return [str_code, Blockly.Python.ORDER_NONE];
};
