App = {};
App.getVarsList = function(){
    var name = Blockly.Variables.allVariables(Blockly.mainWorkspace);
    return name;
}
App.getVars = function(){
    var workspace = Blockly.getMainWorkspace();
    Blockly.Python.init(workspace);
    var blocks = workspace.getTopBlocks(true);
    var codes = [];
    for (var x = 0, block; block = blocks[x]; x++) {

	// 変数を含んだ行のみを出力する。
	var getVariableCode = function(block){
	    var code = [];
	    if(block.type == "variables_set"){
		var func = Blockly.Python[block.type];
		code.push(func.call(block, block));
	    }
	    var blockNext = block.nextConnection && block.nextConnection.targetBlock();
	    var nextCode = [];
	    if(blockNext){
		nextCode = getVariableCode(blockNext);
	    }
	    code = $.merge(code,nextCode);
	    return code;
	}
	codes.push(getVariableCode(block));
    }
    codes = codes[0];
    return codes;
}
App.getCode = function(){
    // Generate JavaScript code and display it.
    window.Blockly.Python.INFINITE_LOOP_TRAP = null;
    var code = window.Blockly.Python.workspaceToCode();
    return code;
}

App.getXml = function(){
    var xmlDom = Blockly.Xml.workspaceToDom(Blockly.mainWorkspace);
    var xmlText = Blockly.Xml.domToPrettyText(xmlDom);
    return xmlText;
}

App.setXml = function(xmlText){
    try {
        xmlDom = Blockly.Xml.textToDom(xmlText);
    } catch (e) {
        var q =window.confirm(MSG['badXml'].replace('%1', e));
        if (!q) {
            // Leave the user on the XML tab.
            return;
        }
    }
    if (xmlDom) {
        Blockly.mainWorkspace.clear();
        Blockly.Xml.domToWorkspace(Blockly.mainWorkspace, xmlDom);
    }
}

App.getSelectingCode = function(){
    var block = Blockly.selected;
    var code = Blockly.Python.blockToCode(block);
    if(code == ""){
        return ""
    }
    var strs = App.getVars().join("\n");
    if(code.length > 1 && typeof code != 'string'){
        return strs+Blockly.Python.multipleCodeToOutput(code[0],"im_output");
    }
    // このコードいる？
    var code_str = code;
    var codeArr = code_str.split("\n");
    codeArr = codeArr.filter(function(element,index,array){return element!=""});
    var lastLine = codeArr[codeArr.length-1];
    if(lastLine.split("=").length > 1){
        //alert(code_str+"im_output = "+lastLine.split("=")[0])
        return strs+code_str+"im_output = "+lastLine.split("=")[0];
    }
    return strs+code;
}

function init(){
    Blockly.inject(document.getElementById('blocklyDiv'), {toolbox: document.getElementById('toolbox')});
    // Let the top-level application know that Blockly is ready.
    Blockly.Xml.domToWorkspace(Blockly.mainWorkspace,
            document.getElementById('startBlocks'));
    window.parent.blocklyLoaded(Blockly,App);
}
