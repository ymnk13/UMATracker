/**
 * @license
 * Visual Blocks Editor
 *
 * Copyright 2012 Google Inc.
 * https://developers.google.com/blockly/
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @fileoverview Colour input field.
 * @author fraser@google.com (Neil Fraser)
 */
'use strict';

goog.provide('Blockly.FieldHSV');

goog.require('Blockly.Field');
goog.require('goog.dom');
goog.require('goog.events');
goog.require('goog.ui.ColorPicker');
goog.require('goog.ui.HsvPalette');
goog.require('goog.style');


/**
 * Class for a colour input field.
 * @param {string} colour The initial colour in '#rrggbb' format.
 * @param {Function} opt_changeHandler A function that is executed when a new
 *     colour is selected.  Its sole argument is the new colour value.  Its
 *     return value becomes the selected colour, unless it is undefined, in
 *     which case the new colour stands, or it is null, in which case the change
 *     is aborted.
 * @extends {Blockly.Field}
 * @constructor
 */
Blockly.FieldHSV = function(colour, opt_changeHandler) {
  Blockly.FieldHSV.superClass_.constructor.call(this, '\u00A0\u00A0\u00A0');

  this.changeHandler_ = opt_changeHandler;
  // Set the initial state.
  this.setValue(colour);

  // By default use the global constants for colours and columns.
  this.colours_ = null;
  this.columns_ = 0;
};
goog.inherits(Blockly.FieldHSV, Blockly.Field);

/**
 * Install this field on a block.
 * @param {!Blockly.Block} block The block containing this field.
 */
Blockly.FieldHSV.prototype.init = function(block) {
  Blockly.FieldHSV.superClass_.init.call(this, block);
  this.borderRect_.style['fillOpacity'] = 1;
  this.setValue(this.getValue());
};

/**
 * Clone this FieldColour.
 * @return {!Blockly.FieldColour} The result of calling the constructor again
 *   with the current values of the arguments used during construction.
 */
Blockly.FieldHSV.prototype.clone = function() {
  return new Blockly.FieldHSV(this.getValue(), this.changeHandler_);
};

/**
 * Mouse cursor style when over the hotspot that initiates the editor.
 */
Blockly.FieldHSV.prototype.CURSOR = 'default';

/**
 * Close the colour picker if this input is being deleted.
 */
Blockly.FieldHSV.prototype.dispose = function() {
  Blockly.WidgetDiv.hideIfOwner(this);
  Blockly.FieldHSV.superClass_.dispose.call(this);
};

/**
 * Return the current colour.
 * @return {string} Current colour in '#rrggbb' format.
 */
Blockly.FieldHSV.prototype.getValue = function() {
  return this.colour_;
};

/**
 * Set the colour.
 * @param {string} colour The new colour in '#rrggbb' format.
 */
Blockly.FieldHSV.prototype.setValue = function(colour) {
  this.colour_ = colour;
  if (this.borderRect_) {
    this.borderRect_.style.fill = colour;
  }
  if (this.sourceBlock_ && this.sourceBlock_.rendered) {
    // Since we're not re-rendering we need to explicitly call
    // Blockly.Realtime.blockChanged()
    Blockly.Realtime.blockChanged(this.sourceBlock_);
    this.sourceBlock_.workspace.fireChangeEvent();
  }
};

/**
 * Get the text from this field.  Used when the block is collapsed.
 * @return {string} Current text.
 */
Blockly.FieldHSV.prototype.getText = function() {
  var colour = this.colour_;
  var m = colour.match(/^#(.)\1(.)\2(.)\3$/);
  if (m) {
    colour = '#' + m[1] + m[2] + m[3];
  }
  return colour;
};

/**
 * An array of colour strings for the palette.
 * See bottom of this page for the default:
 * http://docs.closure-library.googlecode.com/git/closure_goog_ui_colorpicker.js.source.html
 * @type {!Array.<string>}
 */
Blockly.FieldHSV.COLOURS = goog.ui.ColorPicker.SIMPLE_GRID_COLORS;

/**
 * Number of columns in the palette.
 */
Blockly.FieldHSV.COLUMNS = 7;

/**
 * Set a custom colour grid for this field.
 * @param {Array.<string>} colours Array of colours for this block,
 *     or null to use default (Blockly.FieldColour.COLOURS).
 * @return {!Blockly.FieldColour} Returns itself (for method chaining).
 */
Blockly.FieldHSV.prototype.setColours = function(colours) {
  this.colours_ = colours;
  return this;
};

/**
 * Set a custom grid size for this field.
 * @param {number} columns Number of columns for this block,
 *     or 0 to use default (Blockly.FieldColour.COLUMNS).
 * @return {!Blockly.FieldColour} Returns itself (for method chaining).
 */
Blockly.FieldHSV.prototype.setColumns = function(columns) {
  this.columns_ = columns;
  return this;
};

/**
 * Create a palette under the colour field.
 * @private
 */
Blockly.FieldHSV.prototype.showEditor_ = function() {
  Blockly.WidgetDiv.show(this, Blockly.FieldHSV.widgetDispose_);
  // Create the palette using Closure.
  var picker = new goog.ui.HsvPalette();

  // Position the palette to line up with the field.
  // Record windowSize and scrollOffset before adding the palette.
  var windowSize = goog.dom.getViewportSize();
  var scrollOffset = goog.style.getViewportPageOffset(document);
  var xy = Blockly.getAbsoluteXY_(/** @type {!Element} */ (this.borderRect_));
  var borderBBox = this.borderRect_.getBBox();
  var div = Blockly.WidgetDiv.DIV;
  picker.render(div)
    div.setAttribute('style',div.getAttribute('style')+"background-color:#ffffff;")
  // Record paletteSize after adding the palette.
  var paletteSize = goog.style.getSize(picker.getElement());

  // Flip the palette vertically if off the bottom.
  if (xy.y + paletteSize.height + borderBBox.height >=
      windowSize.height + scrollOffset.y) {
    xy.y -= paletteSize.height - 1;
  } else {
    xy.y += borderBBox.height - 1;
  }
  if (Blockly.RTL) {
    xy.x += borderBBox.width;
    xy.x -= paletteSize.width;
    // Don't go offscreen left.
    if (xy.x < scrollOffset.x) {
      xy.x = scrollOffset.x;
    }
  } else {
    // Don't go offscreen right.
    if (xy.x > windowSize.width + scrollOffset.x - paletteSize.width) {
      xy.x = windowSize.width + scrollOffset.x - paletteSize.width;
    }
  }
  Blockly.WidgetDiv.position(xy.x, xy.y, windowSize, scrollOffset);

  // Configure event handler.

  var thisField = this;

  Blockly.FieldHSV.changeEventKey_ = goog.events.listen(picker,
       goog.ui.Component.EventType.ACTION,
       function(event) {
         var colour = event.target.getColor() || '#000000';

         if (thisField.sourceBlock_ && thisField.changeHandler_) {
             // Call any change handler, and allow it to override.
             var override = thisField.changeHandler_(colour);
             if (override !== undefined) {
		 colour = override;
             }
         }
           if (colour !== null) {
               thisField.setValue(colour);
           }
       });

};

/**
 * Hide the colour palette.
 * @private
 */
Blockly.FieldHSV.widgetDispose_ = function() {
  if (Blockly.FieldHSV.changeEventKey_) {
    goog.events.unlistenByKey(Blockly.FieldHSV.changeEventKey_);
  }
};
