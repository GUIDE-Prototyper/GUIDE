import { getKeyByIconName } from '../Assets/Icons_light';

figma.showUI(__html__, { themeColors: true, width: 385, height: 600, title: "GUIDE: LLM-Driven GUI Generation Decomposition for Automated Prototyping" });

figma.ui.onmessage = async msg => {
 
  if (msg.type === "create-preview-multiple") {
    
    if (msg.type === 'close') {
      figma.closePlugin();
    }

    if (msg.data != null && msg.data.length > 0) {
  
      let targetPage = figma.root.findChild(n => n.name === "TempDraw") as PageNode;
      if (msg.draw) targetPage = figma.root.findChild(n => n.name === "Workarea") as PageNode;

      let workFrame = targetPage.findOne(node => node.type === "FRAME" && node.name === msg.frame[0]) as FrameNode;
      let nodesToGroup = [];

      let promises: Promise<void>[] = [];

      for (let item of msg.data) {
          let attributes = item.attributes || null;
          let genAttributes = item.general_attributes || item.generalAttributes;
          let group = item.group || null;
          let key = item.key || genAttributes.key || null;
          let options = item.options || null;
          let type = item.type || null;

          console.log("here", item);
      
          if (key != null && key.length > 0 && key != '-') {
              promises.push(
                  figma.importComponentByKeyAsync(key).then(async component => {
                      let instance = component.createInstance();
  
                      instance = parseGeneralAttrbiutes(instance, genAttributes, type);
      
                      instance = await parseIndividualAttributes(instance, attributes, genAttributes, type);
  
                      if (!msg.draw) targetPage.appendChild(instance);
                      if (msg.draw) workFrame.appendChild(instance);
                      nodesToGroup.push(instance);
                  })
              );
          }
      
          if (type === 'Rectangle') {
            let rect = figma.createRectangle();
            rect = parseGeneralAttrbiutes(rect, genAttributes, type);
                        
            if (!msg.draw) targetPage.appendChild(rect);
            if (msg.draw) workFrame.appendChild(rect);
            nodesToGroup.push(rect);
          }
  
          if (type === 'Label') {
            let text = figma.createText()
            promises.push(setText(text, attributes['Label Text']));
            text = parseGeneralAttrbiutes(text, genAttributes, type);
    
            if (!msg.draw) targetPage.appendChild(text);
            if (msg.draw) workFrame.appendChild(text);
            nodesToGroup.push(text);
          }
  
      }
      
      await Promise.all(promises);
  
      if (!msg.draw) {
        if (nodesToGroup.length > 0){
          let group = figma.group(nodesToGroup, targetPage);
          group.name = "AI for Feature: " + msg.id;
    
          const componentId = group.id;
          const componentName = group.name;
          
          await exportPNG(group).then(val => {
            
          figma.ui.postMessage({
              type: 'COMPONENT_PREVIEW_SELECTED',
              data: {
                id: componentId,
                name: componentName,
                imageUrl: val,
              },
            });
          });
  
        group.remove();
  
        } else {
          figma.ui.postMessage({
            type: 'NO_PREVIEW',
            data: {},
          });
          console.log("Error no items in nodes group");
        }
        
      } else {
        if (nodesToGroup.length > 0){
          let group = figma.group(nodesToGroup, workFrame);
          group.name = "AI for Feature: " + msg.id;
  
          figma.ui.postMessage({
            type: 'COMPONENT_DRAWN',
          });
        } else {
          figma.ui.postMessage({
            type: 'NOTHING_DRAWN',
            data: {},
          });
        }
      }
  
    }
  }

};

function hexToRgb(hex: string, decimal: boolean = false): { r: number, g: number, b: number } {
  hex = hex.replace(/^#/, '');

  const r = parseInt(hex.slice(0, 2), 16);
  const g = parseInt(hex.slice(2, 4), 16);
  const b = parseInt(hex.slice(4, 6), 16);

  if (decimal) {
      return { r: r / 255, g: g / 255, b: b / 255 };
  }

  return { r, g, b };
}

async function exportPNG(node: SceneNode): Promise<string> {
  const bytes = await node.exportAsync({ format: 'PNG' });
  return `data:image/png;base64,${figma.base64Encode(bytes)}`;
}

async function setText(node: TextNode, newText: string) {
  await figma.loadFontAsync(node.fontName as FontName);
  node.characters = newText;
}

function parseGeneralAttrbiutes(instance: any, genAttributes: any, type: string): any  {

  try {
    instance.x = Number(genAttributes["x"] || genAttributes.xPos || 0);
    instance.y = Number(genAttributes.y || genAttributes.yPos || 0);
    instance.resize(Number(genAttributes.width || instance.width), Number(genAttributes.height || instance.height));
    instance.name = genAttributes.name || (type || "Default Name");
    instance.visible = genAttributes.visible !== undefined ? genAttributes.visible : instance.visible;
    instance.cornerRadius = genAttributes.borderRadius !== undefined ? genAttributes.borderRadius :  instance.cornerRadius;
    instance.rotation = genAttributes.rotation !== undefined ? genAttributes.rotation : instance.rotation;
    instance.opacity = genAttributes.opacity !== undefined ? Number(genAttributes.opacity) : instance.opacity;
    instance.minWidth = genAttributes.minWidth !== undefined ? genAttributes.minWidth : null;
    instance.minHeight = genAttributes.minHeight !== undefined ? genAttributes.minHeight : null;
    instance.locked = genAttributes.locked !== undefined ? genAttributes.locked : instance.locked;
    instance.expanded = genAttributes.expanded !== undefined ? genAttributes.expanded : instance.expanded;

    if (genAttributes.color != null) {
      if (genAttributes.color[0].type === 'SOLID') {
        const fills = clone(instance.fills);
        fills[0] = figma.util.solidPaint(genAttributes.color[0].color, fills[0]);
        
        if(genAttributes.color[0].opacity){
          const numberValue = parseFloat(genAttributes.color[0].opacity.replace('%', ''));
          fills[0].opacity = (numberValue / 100);
        }

        instance.fills = fills;
      }
    }

    if (genAttributes.stroke != null) {

      const numberValue = parseFloat(genAttributes.stroke[0].color[0].opacity.replace('%', ''));
      let tempOpacity = (numberValue / 100);

      const newStrokeColor: Paint[] = [{
        type: genAttributes.stroke[0].color[0].type,
        color: hexToRgb(genAttributes.stroke[0].color[0].color, true),
        opacity: tempOpacity,
      }];
      
      instance.strokes = newStrokeColor;
      instance.strokeAlign = genAttributes.stroke[0].align;
    }

    if (genAttributes.effects) {
      const effectsData = genAttributes.effects.map((effect: any) => {
          const { r, g, b } = hexToRgb(effect.color.hex, true);

          return {
              type: effect.type,
              radius: effect.radius,
              visible: effect.visible,
              offset: {
                  x: effect.offset.x,
                  y: effect.offset.y,
              },
              spread: effect.spread,
              blendMode: effect.blendMode,
              showShadowBehindNode: effect.showShadowBehindNode,
              color: {
                  r,
                  g,
                  b,
                  a: effect.color.alpha,
              },
          } as Effect;
      });

      instance.effects = effectsData;
  }

  } catch (error) {
    console.error("Error parsing:", error);
  }

  function clone(val: typeof figma.mixed | readonly Paint[]) {
    return JSON.parse(JSON.stringify(val))
  }

  return instance;
}

async function parseIndividualAttributes(instance: InstanceNode, attributes: any, genAttributes: any, type: string): Promise<InstanceNode> {
  try {
    const updatePromises: any[] = [];

    if (attributes["Label Text"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("label text")) {
            instance.setProperties({ [element]: attributes["Label Text"] });
          }
        }
      } catch (error) {
        console.error("Error setting Label Text:", error);
      }
    }

    if (attributes["Badge label text"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("badge label text")) {
            instance.setProperties({ [element]: attributes["Badge label text"] });
          }
        }
      } catch (error) {
        console.error("Error setting Badge label text:", error);
      }
    }

    if (attributes["Supporting Text"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("supporting text")) {
            instance.setProperties({ [element]: attributes["Supporting Text"] });
          }
        }
      } catch (error) {
        console.error("Error setting Supporting Text:", error);
      }
    }

    if (attributes["Headline Text"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("headline")) {
            instance.setProperties({ [element]: attributes["Headline Text"] });
          }
        }
      } catch (error) {
        console.error("Error setting Headline Text:", error);
      }
    }

    if (attributes["headline"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("headline")) {
            instance.setProperties({ [element]: attributes["headline"] });
          }
        }
      } catch (error) {
        console.error("Error setting Headline Text:", error);
      }
    }

    if (attributes["Show Clear Button"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show clear button")) {
            instance.setProperties({ [element]: (attributes["Show Clear Button"] === true) });
          }
        }
      } catch (error) {
        console.error("Error setting Show Clear Button:", error);
      }
    }

    if (attributes["Show Support Text"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show supporting text")) {
            instance.setProperties({ [element]: attributes["Show Support Text"].length > 0});
          }
        }
      } catch (error) {
        console.error("Error setting Show supporting text:", error);
      }
    }

    if (attributes["Input Text"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("placeholder text")) {
            instance.setProperties({ [element]: attributes["Input Text"]});
          }
        }
      } catch (error) {
        console.error("Error setting Placeholder text:", error);
      }
    }

    if (attributes["Show badge label"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show badge label")) {
            instance.setProperties({ [element]: attributes["Show badge label"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show badge label:", error);
      }
    }

    if (attributes["Section Header"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("section header")) {
            instance.setProperties({ [element]: attributes["Section Header"] });
          }
        }
      } catch (error) {
        console.error("Error setting Section Header:", error);
      }
    }


    if (attributes["Style"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("style")) {
            instance.setProperties({ [element]: attributes["Style"] });
          }
        }
      } catch (error) {
        console.error("Error setting Style:", error);
      }
    }

    if (attributes["State"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("state")) {
            instance.setProperties({ [element]: attributes["State"] });
          }
        }
      } catch (error) {
        console.error("Error setting State:", error);
      }
    }

    if (attributes["Show Icon"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show icon")) {
            instance.setProperties({ [element]: (attributes["Show Icon"] == true)});
          }
        }
      } catch (error) {
        console.error("Error setting Show Icon:", error);
      }
    }

    // List related checks
    if (attributes["Show scrollbar"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show scrollbar")) {
            instance.setProperties({ [element]: attributes["Show scrollbar"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show scrollbar:", error);
      }
    }

    if (attributes["Density"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("density")) {
            instance.setProperties({ [element]: attributes["Density"] });
          }
        }
      } catch (error) {
        console.error("Error setting Density:", error);
      }
    }

    if (attributes["Show trailing element"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show trailing element")) {
            instance.setProperties({ [element]: attributes["Show trailing element"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show trailing element:", error);
      }
    }

    if (attributes["Show leading element"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show leading element")) {
            instance.setProperties({ [element]: attributes["Show leading element"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show leading element:", error);
      }
    }

    if (attributes["Show divider"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show divider")) {
            instance.setProperties({ [element]: attributes["Show divider"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show divider:", error);
      }
    }

    if (attributes["Show trailing supporting text"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show trailing supporting text")) {
            instance.setProperties({ [element]: attributes["Show trailing supporting text"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show trailing supporting text:", error);
      }
    }

    if (attributes["Show leading avatar"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show leading avatar")) {
            instance.setProperties({ [element]: attributes["Show leading avatar"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show leading avatar:", error);
      }
    }

    if (attributes["Show radio button"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show radio button")) {
            instance.setProperties({ [element]: attributes["Show radio button"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show radio button:", error);
      }
    }

    if (attributes["Swap divider type"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("swap divider type")) {
            instance.setProperties({ [element]: attributes["Swap divider type"] });
          }
        }
      } catch (error) {
        console.error("Error setting Swap divider type:", error);
      }
    }

    if (attributes["Show image"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show image")) {
            instance.setProperties({ [element]: attributes["Show image"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show image:", error);
      }
    }

    if (attributes["Overline"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("overline")) {
            instance.setProperties({ [element]: attributes["Overline"] });
          }
        }
      } catch (error) {
        console.error("Error setting Overline:", error);
      }
    }

    if (attributes["Headline"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("headline")) {
            instance.setProperties({ [element]: attributes["Headline"] });
          }
        }
      } catch (error) {
        console.error("Error setting Headline:", error);
      }
    }

    // Bottom App Bar checks
    if (attributes["Show FAB"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show fab")) {
            instance.setProperties({ [element]: attributes["Show FAB"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show FAB:", error);
      }
    }

    // Top App Bar checks
    if (attributes["Show 1st trailing icon"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show 1st trailing icon")) {
            instance.setProperties({ [element]: attributes["Show 1st trailing icon"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show 1st trailing icon:", error);
      }
    }

    if (attributes["Show 2nd trailing icon"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show 2nd trailing icon")) {
            instance.setProperties({ [element]: attributes["Show 2nd trailing icon"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show 2nd trailing icon:", error);
      }
    }

    if (attributes["Show 3rd trailing icon"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show 3rd trailing icon")) {
            instance.setProperties({ [element]: attributes["Show 3rd trailing icon"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show 3rd trailing icon:", error);
      }
    }

    if (attributes["Configuration"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("configuration")) {
            instance.setProperties({ [element]: attributes["Configuration"] });
          }
        }
      } catch (error) {
        console.error("Error setting Configuration:", error);
      }
    }

    if (attributes["Elevation"]) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("elevation")) {
            instance.setProperties({ [element]: attributes["Elevation"] });
          }
        }
      } catch (error) {
        console.error("Error setting Elevation:", error);
      }
    }

    if (attributes["Size"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("size")) {
            instance.setProperties({ [element]: attributes["Size"] });
          }
        }
      } catch (error) {
        console.error("Error setting Size:", error);
      }
    }

    // Segmented Button checks
    if (attributes["Segments"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("segments")) {
            instance.setProperties({ [element]: attributes["Segments"] });
          }
        }
      } catch (error) {
        console.error("Error setting Segments:", error);
      }
    }

    if (attributes["Show video thumbnail"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show video thumbnail")) {
            instance.setProperties({ [element]: attributes["Show video thumbnail"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show video thumbnail:", error);
      }
    }


    if (attributes["Show leading icon"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show leading icon")) {
            instance.setProperties({ [element]: attributes["Show leading icon"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show leading icon:", error);
      }
    }


    if (attributes["Show switch"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show switch")) {
            instance.setProperties({ [element]: attributes["Show switch"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show switch:", error);
      }
    }

    if (attributes["Show checkbox"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show checkbox")) {
            instance.setProperties({ [element]: attributes["Show checkbox"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show checkbox:", error);
      }
    }

    if (attributes["Trailing supporting text"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("trailing supporting text")) {
            instance.setProperties({ [element]: attributes["Trailing supporting text"] });
          }
        }
      } catch (error) {
        console.error("Error setting Trailing supporting text:", error);
      }
    }


    // Icon Button checks
    if (attributes["Icon (selected)"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("icon (selected)")) {
            instance.setProperties({ [element]: attributes["Icon (selected)"] });
          }
        }
      } catch (error) {
        console.error("Error setting Icon (selected):", error);
      }
    }

    if (attributes["Icon (unselected)"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("icon (unselected)")) {
            instance.setProperties({ [element]: attributes["Icon (unselected)"] });
          }
        }
      } catch (error) {
        console.error("Error setting Icon (unselected):", error);
      }
    }


    if (attributes["Show trailing icon"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show trailing icon")) {
            instance.setProperties({ [element]: attributes["Show trailing icon"] });
          }
        }
      } catch (error) {
        console.error("Error setting Show trailing icon:", error);
      }
    }

    if (attributes["Header Text"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("header text")) {
            instance.setProperties({ [element]: attributes["Header Text"] });
          }
        }
      } catch (error) {
        console.error("Error setting Header Text:", error);
      }
    }

    
    if (attributes["Subheader Text"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("subhead text")) {
            instance.setProperties({ [element]: attributes["Subheader Text"] });
          }
        }
      } catch (error) {
        console.error("Error setting Subheader Text:", error);
      }
    }

    // Dialog
    if (attributes["Show Divider"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("show divider")) {
            instance.setProperties({ [element]: attributes["Show Divider"] === "True" });
          }
        }
      } catch (error) {
        console.error("Error setting Show Divider:", error);
      }
    }

    if (attributes["Title Text"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("title#")) {
            instance.setProperties({ [element]: attributes["Title Text"] });
          }
        }
      } catch (error) {
        console.error("Error setting Title Text:", error);
      }
    }

    if (attributes["headline"] != undefined) {
      try {
        for (let element in instance.componentProperties) {
          if (element.toLocaleLowerCase().includes("configuration")) {
            instance.setProperties({ [element]: "Small" });
          }
        }
      } catch (error) {
        console.error("Error setting Headline:", error);
      }
    }
    

    if (attributes["Icon"] != undefined) {
      try {
        updatePromises.push(updateInstanceIcon(instance, getKeyByIconName(attributes["Icon"])));
      } catch (error) {
        console.error("Error setting Icon:", error);
      }
      await Promise.all(updatePromises);
    }

    if (attributes["Leading Icon"] != undefined) {
      try {
        updatePromises.push(updateInstanceIcon(instance, getKeyByIconName(attributes["Leading Icon"])));
      } catch (error) {
        console.error("Error setting Icon:", error);
      }
      await Promise.all(updatePromises);
    }
    
    if (attributes["Trailing Icon"] != undefined) {
      try {
        updatePromises.push(updateInstanceIcon(instance, getKeyByIconName(attributes["Trailing Icon"])));
      } catch (error) {
        console.error("Error setting Icon:", error);
      }
      await Promise.all(updatePromises);
    }

    if (attributes["leading icon"] != undefined) {
      try {
        updatePromises.push(updateInstanceIconWithParameter(instance, getKeyByIconName(attributes["leading icon"]), 'leading-icon'));
      } catch (error) {
        console.error("Error setting Icon:", error);
      }
      await Promise.all(updatePromises);
    }
    
    if (attributes["trailing icon"] != undefined) {
      try {
        updatePromises.push(updateInstanceIconWithParameter(instance, getKeyByIconName(attributes["trailing icon"]), 'trailing-icon'));
      } catch (error) {
        console.error("Error setting Icon:", error);
      }
      await Promise.all(updatePromises);
    }
    
    if (attributes["Icon_Selected"] != undefined) {
      try {
        updatePromises.push(updateInstanceIconWithParameter(instance, getKeyByIconName(attributes["Icon_Selected"]), 'Selected-icon'));
      } catch (error) {
        console.error("Error setting Icon_Selected:", error);
      }
      await Promise.all(updatePromises);
    }

    if (attributes["Icon_unselected"] != undefined) {
      try {
        updatePromises.push(updateInstanceIconWithParameter(instance, getKeyByIconName(attributes["Icon_unselected"]), 'Unselected-icon'));
      } catch (error) {
        console.error("Error setting Icon_unselected:", error);
      }
      await Promise.all(updatePromises);
    }
    

    // Primary and Secondary Action
    if (attributes["Primary Action"] != undefined || attributes["Secondary Action"] != undefined) {
      const secondaryButtonNode = instance.findOne(n => n.type === "INSTANCE" && n.name === "Secondary button");
      const primaryButtonNode = instance.findOne(n => n.type === "INSTANCE" && n.name === "Primary button");

      // Handle Secondary Button
      if (secondaryButtonNode && attributes["Secondary Action"]) {
        const secondaryKey = attributes["Secondary Action"] && attributes["Secondary Action"].general_attributes && attributes["Secondary Action"].general_attributes.key;
        
        if (secondaryKey) {
          const newButtonComponent = await figma.importComponentByKeyAsync(secondaryKey);
          if (newButtonComponent) {
            // @ts-ignore
            secondaryButtonNode.swapComponent(newButtonComponent);

            let updatedSecondaryButtonNode = instance.findOne(n => n.id === secondaryButtonNode.id) as InstanceNode;
            console.log(attributes["Secondary Action"]);

            updatedSecondaryButtonNode = await parseIndividualAttributes(updatedSecondaryButtonNode, attributes["Secondary Action"].attributes, attributes["Secondary Action"].general_attributes, type);
          }
        }
      }

      // Handle Primary Button
      if (primaryButtonNode && attributes["Primary Action"]) {
        const primaryKey = attributes["Primary Action"] && attributes["Primary Action"].general_attributes && attributes["Primary Action"].general_attributes.key;

        if (primaryKey) {
          const newButtonComponent = await figma.importComponentByKeyAsync(primaryKey);
          if (newButtonComponent) {
            // @ts-ignore
            primaryButtonNode.swapComponent(newButtonComponent);

            let updatedPrimaryButtonNode = instance.findOne(n => n.id === primaryButtonNode.id) as InstanceNode;

            updatedPrimaryButtonNode = await parseIndividualAttributes(updatedPrimaryButtonNode, attributes["Primary Action"].attributes, attributes["Primary Action"].general_attributes, type);
          }
        }
      }
    }

    // Segmented Button Details
    if (attributes["Block 1"] || attributes["Block 2"] || attributes["Block 3"] || attributes["Block 4"] || attributes["Block 5"]) {
      const blocks = ["Block 1", "Block 2", "Block 3", "Block 4", "Block 5"];

      blocks.forEach((block, index) => {
        if (attributes[block] && attributes[block].attributes["Text"]) {
          try {
            // @ts-ignore
            const instanceChild: InstanceNode = instance.children[index];

            if (instanceChild && instanceChild.componentProperties) {
              for (let element in instanceChild.componentProperties) {
                if (element.toLocaleLowerCase().includes("text")) {
                  instanceChild.setProperties({ [element]: attributes[block].attributes["Text"] });
                }
                if (element.toLocaleLowerCase().includes("configuration")) {
                  instanceChild.setProperties({ [element]: attributes[block].options["Configuration"] });
                }
                if (element.toLocaleLowerCase().includes("selected")) {
                  instanceChild.setProperties({ [element]: attributes[block].options["Selected"] });
                }
                if (element.toLocaleLowerCase().includes("state")) {
                  instanceChild.setProperties({ [element]: attributes[block].options["Style"] });
                }
              }
              if (attributes[block].attributes["Icon"]) {
                updatePromises.push(updateInstanceIcon(instanceChild, getKeyByIconName(attributes[block].attributes["Icon"])));
              }
            }
          } catch (error) {
            console.error(`Error processing ${block}:`, error);
          }
        }
      });

      await Promise.all(updatePromises);
    }

    // Tabs, Tab Bar
    if (attributes["Tab 1"] || attributes["Tab 2"] || attributes["Tab 3"] || attributes["Tab 4"] || attributes["Tab 5"]) {
      const blocks = ["Tab 1", "Tab 2", "Tab 3", "Tab 4", "Tab 5"];

      blocks.forEach((block, index) => {
        if (attributes[block]) {
          try {
            // @ts-ignore
            let instanceChild: InstanceNode = instance.children[0].children[index];

            if (instanceChild && instanceChild.componentProperties) {
              for (let element in instanceChild.componentProperties) {
                instanceChild.visible = true;

                if (element.toLocaleLowerCase().includes("badge label")) {
                  instanceChild.setProperties({ [element]: attributes[block].attributes["Badge Label"] });
                }
                if (element.toLocaleLowerCase().includes("badge size")) {
                  instanceChild.setProperties({ [element]: attributes[block].attributes["Badge Size"] });
                }
                if (element.toLocaleLowerCase().includes("label text")) {
                  instanceChild.setProperties({ [element]: attributes[block].attributes["Label text"] });
                }
                if (element.toLocaleLowerCase().includes("show badge")) {
                  instanceChild.setProperties({ [element]: (attributes[block].attributes["Show Badge"] == true) });
                }

                if (element.toLocaleLowerCase().includes("selected")) {
                  instanceChild.setProperties({ [element]: attributes[block].options["Selected"] });
                }
                if (element.toLocaleLowerCase().includes("state")) {
                  instanceChild.setProperties({ [element]: attributes[block].options["State"] });
                }
              }
              if (attributes[block].attributes["Icon"]) {
                updatePromises.push(updateInstanceIcon(instanceChild, getKeyByIconName(attributes[block].attributes["Icon"])));
              }
            }

          } catch (error) {
            console.error(`Error processing ${block}:`, error);
          }
        }
      });

      await Promise.all(updatePromises);
    }

    if (attributes['List']) {
       if (attributes['List'].attributes['List Items']) {

        // @ts-ignore
        let instanceListElements: InstanceNode[] = instance.children[1].children;
        let counterListElements: number = 0;

          for (let listItem of attributes['List'].attributes['List Items']){
            instanceListElements[counterListElements].visible = true;

            console.log(listItem.attributes["Headline Text"]);
            try {
              let instanceChild: InstanceNode = instanceListElements[counterListElements];
  
              if (instanceChild && instanceChild.componentProperties) {
                for (let element in instanceChild.componentProperties) {
                  instanceChild.visible = true;
                  
                  // Attributes
                  if (element.toLocaleLowerCase().includes("headline#")) {
                    instanceChild.setProperties({ [element]: listItem.attributes["Headline Text"] });
                  }

                  // Options
                  if (element.toLocaleLowerCase().includes("condition")) {
                    instanceChild.setProperties({ [element]: listItem.options["Condition"] });
                  }
                  if (element.toLocaleLowerCase() == "leading") {
                    instanceChild.setProperties({ [element]: listItem.options["Leading"] });
                  }
                  if (element.toLocaleLowerCase().includes("show overline")) {
                    instanceChild.setProperties({ [element]: (listItem.options["Show overline"] === true) });
                  }
                  if (element.toLocaleLowerCase().includes("show trailing supporting text")) {
                    instanceChild.setProperties({ [element]: (listItem.options["Show trailing supporting text"] === true)});
                  }
                  if (element.toLocaleLowerCase() == "trailing") {
                    instanceChild.setProperties({ [element]: listItem.options["Trailing"] });
                  }
                }
                if (attributes['List'].attributes['List Items'].attributes["Icon"]) {
                  updatePromises.push(updateInstanceIcon(instanceChild, getKeyByIconName(attributes['List'].attributes['List Items'].attributes["Icon"])));
                }
              }
  
            } catch (error) {
              console.error(`Error processing ${listItem}:`, error);
            }

            counterListElements++;
          }

          for (let j = counterListElements; j < instanceListElements.length; j++){
            instanceListElements[j].visible = false;
          }
       }
  
      await Promise.all(updatePromises);  
    } 

    // Handle List Items
    if (attributes['List Items']) {

      // @ts-ignore
       let instanceListElements: InstanceNode[] = instance.children;
       let counterListElements: number = 0;

         for (let listItem of attributes['List Items']){
           instanceListElements[counterListElements].visible = true;

           console.log(listItem.attributes["Headline Text"]);
           try {
             let instanceChild: InstanceNode = instanceListElements[counterListElements];
 
             if (instanceChild && instanceChild.componentProperties) {
               for (let element in instanceChild.componentProperties) {
                 instanceChild.visible = true;
                 
                 // Attributes
                 if (element.toLocaleLowerCase().includes("headline#")) {
                   instanceChild.setProperties({ [element]: listItem.attributes["Headline Text"] });
                 }

                 // Options
                 if (element.toLocaleLowerCase().includes("condition")) {
                   instanceChild.setProperties({ [element]: listItem.options["Condition"] });
                 }
                 if (element.toLocaleLowerCase() == "leading") {
                   instanceChild.setProperties({ [element]: listItem.options["Leading"] });
                 }
                 if (element.toLocaleLowerCase().includes("show overline")) {
                   instanceChild.setProperties({ [element]: (listItem.options["Show overline"] === true) });
                 }
                 if (element.toLocaleLowerCase().includes("show trailing supporting text")) {
                   instanceChild.setProperties({ [element]: (listItem.options["Show supporting text"] === true)});
                 }
                 if (element.toLocaleLowerCase() == "trailing") {
                   instanceChild.setProperties({ [element]: listItem.options["Trailing"] });
                 }
               }
               if (attributes['List Items'].attributes["Icon"]) {
                 updatePromises.push(updateInstanceIcon(instanceChild, getKeyByIconName(attributes['List Items'].attributes["Icon"])));
               }
             }
 
           } catch (error) {
             console.error(`Error processing ${listItem}:`, error);
           }

           counterListElements++;
         }

         // Set visiblity of others to false
         for (let j = counterListElements; j < instanceListElements.length; j++){
           instanceListElements[j].visible = false;
         }
         await Promise.all(updatePromises); 
    } 
  } catch (error) {
    console.error("Error in main try block:", error);
  }

  console.log('Created Instance', instance);
  return instance;
}

async function updateInstanceIcon(instance: InstanceNode, newIconComponentKey: string) {
  const iconInstance = instance.findOne(node => node.type === "INSTANCE" && (node.name.includes("Icon") || node.name.includes("Selected icon") || node.name === ("icon") || node.name === ("leading-icon") || node.name === ("trailing-icon") || node.name === ("Selected-icon") || node.name === ("Unselected-icon")) );

  if (iconInstance && iconInstance.type === "INSTANCE") {
    const newIconComponent = await figma.importComponentByKeyAsync(newIconComponentKey);
    iconInstance.swapComponent(newIconComponent);
  }

  if (
    (iconInstance && (iconInstance.name === "trailing-icon" || iconInstance.name === "leading-icon")) &&
    iconInstance.isAsset === false
  ) {
    
    // @ts-ignore#
    const iconInstanceChild = iconInstance.findOne(node => node.type === "INSTANCE" && (node.name.includes("Icon") || node.name.includes("Selected icon") || node.name === ("icon") || node.name === ("leading-icon") || node.name === ("trailing-icon") || node.name === ("Selected-icon") || node.name === ("Unselected-icon")) );
    const newIconComponent = await figma.importComponentByKeyAsync(newIconComponentKey);
    iconInstanceChild.swapComponent(newIconComponent);
  }
}

async function updateInstanceIconWithParameter(instance: InstanceNode, newIconComponentKey: string, parameter: string) {
  const iconInstance = instance.findOne(node => node.type === "INSTANCE" && (node.name === parameter) );

  if (iconInstance && iconInstance.type === "INSTANCE") {
    const newIconComponent = await figma.importComponentByKeyAsync(newIconComponentKey);
    iconInstance.swapComponent(newIconComponent);
  }

  if (
    iconInstance != null && 
    (iconInstance.name === "trailing-icon" || iconInstance.name === "leading-icon") && 
    iconInstance.isAsset === false
  ) {
    
    // @ts-ignore
    const iconInstanceChild = iconInstance.findOne(node => node.type === "INSTANCE" && (node.name === parameter ));
    const newIconComponent = await figma.importComponentByKeyAsync(newIconComponentKey);
    iconInstanceChild.swapComponent(newIconComponent);
  }
}