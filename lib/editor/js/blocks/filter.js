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
    var value_img = Blockly.Python.valueToCode(block, 'img', Blockly.Python.ORDER_NONE);
    // TODO: Assemble Python into code variable.
    var code = Blockly.Python.joinCodesToOperator(value_img, '', 'cv2.cvtColor({0},cv2.COLOR_BGR2GRAY)\n');

    // TODO: Change ORDER_NONE to the correct strength.
    return [code, Blockly.Python.ORDER_NONE];
};


Blockly.Blocks['im_threshold'] = {
    init: function() {
        this.setHelpUrl('http://www.example.com/');
        this.appendValueInput("im_threshold")
            .appendField("Threshold :")
            .appendField(new Blockly.FieldTextInput("100"), "threshold");
        this.setOutput(true);
        this.setTooltip('');
    }
};

Blockly.Python['im_threshold'] = function(block) {
    var value_im_threshold = Blockly.Python.valueToCode(block, 'im_threshold', Blockly.Python.ORDER_NONE);
    var text_threshold = block.getFieldValue('threshold');
    // TODO: Assemble Python into code variable.
    var code = 'cv2.threshold({0},{1},255,cv2.THRESH_BINARY)[1]\n'.format('{0}',text_threshold);
    var codeResult = Blockly.Python.joinCodesToOperator(value_im_threshold,'',code);
    // TODO: Change ORDER_NONE to the correct strength.
    return [codeResult, Blockly.Python.ORDER_NONE];
};


Blockly.Blocks['im_threshold_trunc'] = {
    init: function() {
        this.setHelpUrl('http://www.example.com/');
        this.appendValueInput("im_threshold_trunc")
            .appendField("Threshold Trunc :")
            .appendField(new Blockly.FieldTextInput("100"), "threshold");
        this.setOutput(true);
        this.setTooltip('');
    }
};

Blockly.Python['im_threshold_trunc'] = function(block) {
    var value_im_threshold = Blockly.Python.valueToCode(block, 'im_threshold_trunc', Blockly.Python.ORDER_NONE);
    var text_threshold = block.getFieldValue('threshold');
    // TODO: Assemble Python into code variable.
    var code = 'cv2.threshold({0},{1},255,cv2.THRESH_TRUNC)[1]\n'.format('{0}',text_threshold);
    var codeResult = Blockly.Python.joinCodesToOperator(value_im_threshold,'',code);
    // TODO: Change ORDER_NONE to the correct strength.
    return [codeResult, Blockly.Python.ORDER_NONE];
};



Blockly.Blocks['colorFilter_colorSelector'] = {
    init: function() {
        this.setHelpUrl('http://www.example.com/');
        this.appendValueInput("inputA")
            .appendField(new Blockly.FieldHSV("#ff0000"), "Color")
            .appendField("Distance :")
            .appendField(new Blockly.FieldTextInput("100"), "Distance");
        this.setOutput(true);
        this.setTooltip('');
    }
};


Blockly.Python['colorFilter_colorSelector'] = function(block) {
    var value_inputA = Blockly.Python.valueToCode(block, 'inputA', Blockly.Python.ORDER_NONE);
    var colour_color = block.getFieldValue('Color');
    var lab_dist     = parseInt(block.getFieldValue('Distance'));

    var hexToRgb = function (hex) {
        var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? $.map(result,function(v,index){
            if(index == 0)
                return null;
            return parseInt(v,16)
        }) :null;
    };

    var rgb = hexToRgb(colour_color);

    // TODO: Assemble Python into code variable.
    var code = 'filters.colorFilter({0},[{1}],{2})'.format('{0}', rgb, lab_dist);
    var codeResult = Blockly.Python.joinCodesToOperator(value_inputA,'',code);

    // TODO: Change ORDER_NONE to the correct strength.
    return [codeResult, Blockly.Python.ORDER_NONE];
};

Blockly.Blocks['img_inverse'] = {
    init: function() {
        this.setHelpUrl('http://www.example.com/');
        this.appendValueInput("img")
            //.setCheck("Image_BGR")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("Color Inversion");
        this.setOutput(true, "Image_BGR");
        this.setTooltip('');
    }
};

Blockly.Python['img_inverse'] = function(block) {
    var value_img = Blockly.Python.valueToCode(block, 'img', Blockly.Python.ORDER_NONE);
    // TODO: Assemble Python into code variable.
    var code = Blockly.Python.joinCodesToOperator(value_img, '', '~{0}\n');

    // TODO: Change ORDER_NONE to the correct strength.
    return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Blocks['img_median'] = {
    init: function() {
        this.setHelpUrl('http://www.example.com/');
        this.appendValueInput("inputA")
            //.appendField(new Blockly.FieldHSV("#ff0000"), "Color")
            .appendField("MedianFilter :")
            .appendField(new Blockly.FieldTextInput("0"), "Degree");
        this.setOutput(true);
        this.setTooltip('');
    }
};


Blockly.Python['img_median'] = function(block) {
    var value_inputA = Blockly.Python.valueToCode(block, 'inputA', Blockly.Python.ORDER_NONE);
    var degree     = parseInt(block.getFieldValue('Degree'))*2+1;

    // TODO: Assemble Python into code variable.
    var code = 'cv2.medianBlur({0},{1})'.format('{0}', degree);
    var codeResult = Blockly.Python.joinCodesToOperator(value_inputA,'',code);
    console.log(codeResult);
    // TODO: Change ORDER_NONE to the correct strength.
    return [codeResult, Blockly.Python.ORDER_NONE];
};


Blockly.Blocks['img_blur'] = {
    init: function() {
        this.setHelpUrl('http://www.example.com/');
        this.appendValueInput("inputA")
            //.appendField(new Blockly.FieldHSV("#ff0000"), "Color")
            .appendField("BlurFilter :")
            .appendField(new Blockly.FieldTextInput("0"), "Degree")
	    .appendField(" >= 0");
        this.setOutput(true);
        this.setTooltip('');
    }
};


Blockly.Python['img_blur'] = function(block) {
    var value_inputA = Blockly.Python.valueToCode(block, 'inputA', Blockly.Python.ORDER_NONE);
    var degree     = (parseInt(block.getFieldValue('Degree'))+1)*5;

    // TODO: Assemble Python into code variable.
    var code = 'cv2.blur({0},({1},{1}))'.format('{0}', degree);
    var codeResult = Blockly.Python.joinCodesToOperator(value_inputA,'',code);
    console.log(codeResult);
    // TODO: Change ORDER_NONE to the correct strength.
    return [codeResult, Blockly.Python.ORDER_NONE];
};
