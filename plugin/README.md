# Figma Plug-in: Template Based on Esbuild React

This plug-in for Figma is built upon the [esbuild-react example from Figma's plugin samples](https://github.com/figma/plugin-samples/tree/master/esbuild-react), which is published under the MIT license.

## Overview

This Figma plug-in utilizes two specific pages, `Workarea` and `TempDraw`, to manage the plug-in's visual workflow within a Figma file. 

### Key Features
- **Temporary Drawings**: Uses a hidden page (`TempDraw`) for rendering and processing previews.
- **Fixed Naming Conventions**: Relies on predefined page and frame names for proper functionality.
- **GUI Component Handling**: Draws components within a specified frame (`Exercise_1`) in the `Workarea` page.

## Plug-in Setup for Figma

Follow these steps to set up the plug-in:

1. Enter server credentials in `./Config/config.json`.
2. Set the server domain in `manifest.json`.
3. Create a plug-in within Figma (Desktop version) using the manifest from this plug-in as a basis. Ensure that you align the manifest configuration with your custom settings.

## Figma File Requirements

To ensure proper operation, the following structure must be adhered to:

### 1. Pages:
- **Workarea**: This page will serve as the primary workspace. The plug-in will render components within this page.
- **TempDraw**: This page should remain hidden. It will be used to briefly draw previews, which are rendered as PNG images and then deleted automatically.

### 2. Frames:
- **Exercise_1**: This frame must be present on the `Workarea` page. All graphical user interface (GUI) components will be drawn here by the plug-in.

---

Make sure your Figma file is set up with the required pages and frames before using the plug-in to avoid any errors.

## License

This plug-in is licensed under the MIT License. See the [LICENSE](https://github.com/figma/plugin-samples?tab=MIT-1-ov-file#readme) file for more details.