Blockly.Blocks['rectRegionSelector_regionSelector'] = {
    init: function() {
        this.appendValueInput("NAME")
            .appendField("Rectangle Selection")
            .appendField(new Blockly.FieldTextInput("[[0.1, 0.1], [0.9, 0.9]]"), "array");

        this.setOutput(true);
        this.setTooltip('');
        this.setHelpUrl('http://www.example.com/');
        for (var i = 0, input; input = this.inputList[i]; i++) {
            for (var j = 0, field; field = input.fieldRow[j]; j++) {
                if(field.EDITABLE){
                    field.setVisible(false);
                }
            }
        }
    }
};

Blockly.Python['rectRegionSelector_regionSelector'] = function(block) {
    var array = '[[int(x[0]*self.width), int(x[1]*self.height)] for x in {0}]'.format(block.getFieldValue('array'));
    var value_input = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_NONE);

    // TODO: Assemble Python into code variable.
    var code = [];

    var im_mask_name = "self.im_mask_{0}".format(orgFunc.randStr());
    code.push('#self.height, self.width, self.dim = {input}.shape\r\n');
    code.push('#{0} = np.zeros((self.height, self.width), dtype=np.uint8)\r\n'.format(im_mask_name));

    var topTuple = "({0}[0][0], {0}[0][1])".format(array);
    var bottomTuple = "({0}[1][0], {0}[1][1])".format(array);
    code.push('#cv2.rectangle({0}, {1}, {2}, color=255 ,thickness=-1)\r\n'.format(im_mask_name, topTuple, bottomTuple));

    code.push(Blockly.Python.joinCodesToOperator(value_input,im_mask_name,'cv2.bitwise_and({0},{0},mask={1})'));

    // TODO: Change ORDER_NONE to the correct strength.
    var str_code =code.join("\n");
    return [str_code, Blockly.Python.ORDER_NONE];
};



Blockly.Blocks['ellipseRegionSelector_regionSelector'] = {
    init: function() {
        this.appendValueInput("NAME")
            .appendField("Circular Selection")
            .appendField(new Blockly.FieldTextInput("[[0.1, 0.1], [0.9, 0.9]]"), "array");


        this.setOutput(true);
        this.setTooltip('');
        this.setHelpUrl('http://www.example.com/');
        for (var i = 0, input; input = this.inputList[i]; i++) {
            for (var j = 0, field; field = input.fieldRow[j]; j++) {
                if(field.EDITABLE){
                    field.setVisible(false);
                }
            }
        }
    }
};



Blockly.Python['ellipseRegionSelector_regionSelector'] = function(block) {
    var array = '[[x[0]*self.width, x[1]*self.height] for x in {0}]'.format(block.getFieldValue('array'));
    var value_input = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_NONE);

    // TODO: Assemble Python into code variable.
    var code = [];

    var im_mask_name = "self.im_mask_{0}".format(orgFunc.randStr());
    code.push('#self.height, self.width, self.dim = {input}.shape\r\n');
    code.push('#{0} = np.zeros((self.height, self.width), dtype=np.uint8)\r\n'.format(im_mask_name));

    var center = '(int(({0}[0][0]+{0}[1][0])/2), int(({0}[0][1]+{0}[1][1])/2))'.format(array);
    var axes = '(int(abs(({0}[0][0]-{0}[1][0])/2)), int(abs(({0}[0][1]-{0}[1][1])/2)))'.format(array);
    code.push('#cv2.ellipse({0}, {1}, {2}, angle = 0,startAngle = 0,endAngle = 360 , color=255, thickness = -1)\r\n'.format(im_mask_name, center, axes));

    code.push(Blockly.Python.joinCodesToOperator(value_input, im_mask_name, 'cv2.bitwise_and({0},{0},mask={1})'));

    // TODO: Change ORDER_NONE to the correct strength.
    var str_code =code.join("\n");
    return [str_code, Blockly.Python.ORDER_NONE];
};
