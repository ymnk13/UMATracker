function blocklyLoaded(blockly) {
	// Called once Blockly is fully loaded.
	window.Blockly = blockly;
}

function getCode() {
	// Generate JavaScript code and display it.
	window.Blockly.Python.INFINITE_LOOP_TRAP = null;
	var code = window.Blockly.Python.workspaceToCode();
	return code;
}
