Blockly.Blocks['rectRegionSelector_regionSelector'] = {
    init: function() {
        this.appendValueInput("NAME")
            .appendField("短形選択")
            .appendField(new Blockly.FieldTextInput("150"), "topX")
            .appendField(new Blockly.FieldTextInput("150"), "topY")

            .appendField(new Blockly.FieldTextInput("450"), "bottomX")
            .appendField(new Blockly.FieldTextInput("450"), "bottomY")


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
    var text_topx = block.getFieldValue('topX');
    var text_topy = block.getFieldValue('topY');
    var text_bottomx = block.getFieldValue('bottomX');
    var text_bottomy = block.getFieldValue('bottomY');
    var value_input = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_NONE);

    // TODO: Assemble Python into code variable.
    var code = [];

    var im_mask_name = "self.im_mask_{0}".format(orgFunc.randStr());
    code.push('#self.width, self.height, self.dim = {input}.shape\r\n');

    code.push('#{0} = np.zeros((self.width, self.height), dtype=np.uint8)\r\n'.format(im_mask_name));
    code.push('#cv2.rectangle({4},({0},{1}),({2},{3}) , color=255 ,thickness=-1)\r\n'.format(text_topx,text_topy,text_bottomx,text_bottomy,im_mask_name));

    code.push(Blockly.Python.joinCodesToOperator(value_input,im_mask_name,'cv2.bitwise_and({0},{0},mask={1})'));

    // TODO: Change ORDER_NONE to the correct strength.
    var str_code =code.join("\n");
    return [str_code, Blockly.Python.ORDER_NONE];
};



Blockly.Blocks['ellipseRegionSelector_regionSelector'] = {
    init: function() {
        this.appendValueInput("NAME")
            .appendField("円形選択")
            .appendField(new Blockly.FieldTextInput("150"), "topX")
            .appendField(new Blockly.FieldTextInput("150"), "topY")

            .appendField(new Blockly.FieldTextInput("450"), "bottomX")
            .appendField(new Blockly.FieldTextInput("450"), "bottomY")


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
    var text_topx = block.getFieldValue('topX');
    var text_topy = block.getFieldValue('topY');
    var text_bottomx = block.getFieldValue('bottomX');
    var text_bottomy = block.getFieldValue('bottomY');
    var value_input = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_NONE);

    // TODO: Assemble Python into code variable.
    var code = [];

    var im_mask_name = "self.im_mask_{0}".format(orgFunc.randStr());
    code.push('#self.width, self.height, self.dim = {input}.shape\r\n');

    code.push('#{0} = np.zeros((self.width, self.height), dtype=np.uint8)\r\n'.format(im_mask_name));
    code.push('#cv2.ellipse({4},(({0}+{2})/2,({1}+{3})/2),(int(abs(({0}-{2})/2)),int(abs(({1}-{3})/2))), angle = 0,startAngle = 0,endAngle = 360 , color=255,thickness = -1)\r\n'.format(text_topx, text_topy, text_bottomx, text_bottomy, im_mask_name));

    code.push(Blockly.Python.joinCodesToOperator(value_input, im_mask_name, 'cv2.bitwise_and({0},{0},mask={1})'));

    // TODO: Change ORDER_NONE to the correct strength.
    var str_code =code.join("\n");
    return [str_code, Blockly.Python.ORDER_NONE];
};
