App = {};

App.getCode = function(){
    // Generate JavaScript code and display it.
    window.Blockly.Python.INFINITE_LOOP_TRAP = null;
    var code = window.Blockly.Python.workspaceToCode();
    return code;
}

App.getCodeFromSelectedBlock = function(){
    var block = Blockly.selected;
    var code = Blockly.Python.blockToCode(block);
    if(code == ""){
        return ""
    }
    var strs = window.Blockly.Python.workspaceToCode()+"\n";
    if(code.length > 1 && typeof code != 'string'){
        return strs+Blockly.Python.multipleCodeToOutput(code[0],"{output}");
    }
    // このコードいる？
    var code_str = code;
    var codeArr = code_str.split("\n");
    codeArr = codeArr.filter(function(element,index,array){return element!=""});
    var lastLine = codeArr[codeArr.length-1];
    if(lastLine.split("=").length > 1){
        //alert(code_str+"im_output = "+lastLine.split("=")[0])
        return strs+code_str+"{output} = "+lastLine.split("=")[0];
    }
    return strs+code;
}

App.getBlockData = function(){
    var xmlDom = Blockly.Xml.workspaceToDom(Blockly.mainWorkspace);
    var xmlText = Blockly.Xml.domToPrettyText(xmlDom);
    return xmlText;
}

App.setBlockData = function(xmlText,clearFlag){
    clearFlag = typeof clearFlag !== 'undefined' ? clearFlag : true;
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
        if(clearFlag){
            Blockly.mainWorkspace.clear();
        }
        Blockly.Xml.domToWorkspace(Blockly.mainWorkspace, xmlDom);
    }
}

App.setColorThreshold = function(value){
    var xmlText = '\
                  <xml xmlns="http://www.w3.org/1999/xhtml">\
                  <block type="color_filter" id="11" inline="false" x="85" y="221">\
                  <field name="Color">{0}</field>\
                  <field name="Distance">100</field>\
                  </block>\
                  </xml>\
                  ';

    App.setBlockData(xmlText.format(value),false);
}

function init(){
    Blockly.inject(document.getElementById('blocklyDiv'), {toolbox: document.getElementById('toolbox')});
    // Let the top-level application know that Blockly is ready.
    Blockly.Xml.domToWorkspace(Blockly.mainWorkspace,
            document.getElementById('startBlocks'));
    window.parent.blocklyLoaded(Blockly,App);
}
