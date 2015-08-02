Blockly.Blocks['im_RectForAreaSelect'] = {
    init: function() {
	this.appendValueInput("NAME")
            .appendField("Rectangle Top(X,Y)=(")
            .appendField(new Blockly.FieldTextInput("150"), "topX")
            .appendField(",")
            .appendField(new Blockly.FieldTextInput("150"), "topY")
            .appendField(")")
            .appendField("\n\rBottom(X,Y)=")
            .appendField(new Blockly.FieldTextInput("450"), "bottomX")
            .appendField(",")
            .appendField(new Blockly.FieldTextInput("450"), "bottomY")
            .appendField(")");
	this.setOutput(true);
	this.setTooltip('');
	this.setHelpUrl('http://www.example.com/');
    }
};

Blockly.Python['im_RectForAreaSelect'] = function(block) {
    var text_topx = block.getFieldValue('topX');
    var text_topy = block.getFieldValue('topY');
    var text_bottomx = block.getFieldValue('bottomX');
    var text_bottomy = block.getFieldValue('bottomY');
    var value_input = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_ATOMIC);
    // TODO: Assemble Python into code variable.
    var code = [];
    var im_mask_name = "self.im_mask_{0}".format(orgFunc.randStr());
    code.push('#self.width, self.height, self.dim = {input}.shape\r\n');
    code.push('#{0} = np.zeros((self.width, self.height,self.dim), dtype=np.uint8)\r\n'.format(im_mask_name));
    code.push("#color_dim = (255) if self.dim == 1 else (255,255,255)\n")
    code.push('#cv2.rectangle({4},({0},{1}),({2},{3}) , color = color_dim ,thickness = -1)\r\n'.format(text_topx,text_topy,text_bottomx,text_bottomy,im_mask_name));
    code.push('{0} = ~{0}\n'.format(im_mask_name));
    code.push(Blockly.Python.joinCodesToOperator(value_input,im_mask_name,'cv2.bitwise_or({0},{1})'));
    console.log(code);
    var str_code =code.join("\n");
    // TODO: Change ORDER_NONE to the correct strength.
    return [str_code, Blockly.Python.ORDER_NONE];
};
