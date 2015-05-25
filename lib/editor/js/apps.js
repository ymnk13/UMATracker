App = {};
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
    var code = Blockly.Python.blockToCode(block)
    if(code == ""){
	return ""
    }
    var strs = window.Blockly.Python.workspaceToCode()+"\n";
    if(code.length > 1 && typeof code != 'string'){
	return strs+Blockly.Python.multipleCodeToOutput(code[0],"im_output");
    }
    // このコードいる？
    var code_str = code
    var codeArr = code_str.split("\n")
    codeArr = codeArr.filter(function(element,index,array){return element!=""});
    var lastLine = codeArr[codeArr.length-1]
    if(lastLine.split("=").length > 1){
	//alert(code_str+"im_output = "+lastLine.split("=")[0])
	return strs+code_str+"im_output = "+lastLine.split("=")[0]
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
