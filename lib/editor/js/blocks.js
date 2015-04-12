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
if(!orgFunc){
    var orgFunc = {};
    orgFunc.randStr = function(){
	// ランダム文字列(数字+abc)
	return Math.random().toString(36).slice(-8)
    };
}

 
Blockly.Blocks['comment'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.appendValueInput("comment")
        .appendField(new Blockly.FieldTextInput("コメント"), "Comment");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('');
  }
};

Blockly.Python['comment'] = function(block) {
  var value_comment = Blockly.Python.valueToCode(block, 'comment', Blockly.Python.ORDER_ATOMIC);
  var text_comment = block.getFieldValue('Comment');
  // TODO: Assemble Python into code variable.
  var code = '# {0}'.format(text_comment);
  return code;
};

