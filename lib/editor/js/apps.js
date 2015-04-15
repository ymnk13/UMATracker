App = {};
App.getCode = function(){
    // Generate JavaScript code and display it.
    window.Blockly.Python.INFINITE_LOOP_TRAP = null;
    var code = window.Blockly.Python.workspaceToCode();
    return code;
}

function init(){
	Blockly.inject(document.getElementById('blocklyDiv'), {toolbox: document.getElementById('toolbox')});
	// Let the top-level application know that Blockly is ready.
	Blockly.Xml.domToWorkspace(Blockly.mainWorkspace,
			document.getElementById('startBlocks'));
	window.parent.blocklyLoaded(Blockly,App);
}
