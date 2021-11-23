# Breeze Icons

## Introduction

Breeze-icons is a freedesktop.org compatible icon theme. It's developed by the
KDE Community as part of KDE Frameworks 5 and it's used by default in KDE Plasma
5 and KDE Applications.

## Guidelines

The Breeze icons guidelines are described at
[develop.kde.org/hig](https://develop.kde.org/hig).

### Web Usage

Breeze Icons can be used as a webfont from
[cdn.kde.org/breeze-icons/icons.html](https://cdn.kde.org/breeze-icons/icons.html).

```html
<i class="icon icon_icon-name"></i>
```

## Writing Recipes

Many icons are built from templates and component files, assembled using
recipes. Recipes describe how an icon should be assembled, and may also specify
case-by-case modifications.

To make best use of the cookbook system, knowledge of CSS selectors is highly
reccomended, as they are used frequently. [You can find a guide here.](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors)

Due to a limitation of configuration files, `=` cannot be used in CSS selectors.
Instead of `=` you can instead use `::`.

Without knowing CSS, you can probably get by using copy-and-paste.

Below is an example of a minimal cookbook with three recipes:

```ini
[Cookbook]
  context=Generic
  folder=generic
  sizes=32,64

[CookbookColors]
  common-red="#FF0000"
  common-blue="#0000FF"

[framed-balloon-red]
  aliases=
    framed-balloon,
    framed-balloon-rouge
  template=template/picture-frame
  replace["#frame-contents"]=emblems/balloon
  attr["#balloon"]["fill"]="@common-red"

[framed-balloon-blue]
  aliases=framed-balloon-indigo
  template=template/picture-frame
  replace["#frame-contents"]=emblems/balloon
  attr["#balloon"]["fill"]="@common-blue"

[framed-balloon-adaptive]
  template=template/picture-frame
  replace["#frame-contents"]=emblems/balloon
  classes["#balloon"]="+ColorScheme-Highlight"
  attr["#balloon"]["fill"]="currentColor"

```
Lets go line-by-line:

```ini
[Cookbook]
```

Holds information that applies to all icons produced in the cookbook. It
includes 3 main values:

 - `context`: The "pretty name" of the context. Common contexts include
   "Mimetypes", "Places", "Apps", etc.
 - `folder`: Usually the same as the context, but lower case. This is the
   top-level folder the various sizes of icons will be placed in.
 - `sizes`: A comma-separated list of sizes. Every recipe in this cookbook
   generates multiple icons.

```ini
[CookbookColors]
```
Contains commonly used color values. Colors are referenced
with `@` in other areas of the cookbook.

Note that both `Cookbook` and `CookbookColors` are reserved sections. All other
sections in the cookbook refer to individual icons.

```ini
[framed-balloon-red]
```
Denotes that an icon with the filename
"framed-balloon-red.svg" should be created for every size in the specified
folder from `[Cookbook]`.

In the example above, the build folder will result in a structure like so:
 - build/
   - generic/
     - 32/
       - framed-balloon.svg _(shortcut to framed-balloon-red.svg)_
       - framed-balloon-adaptive.svg
       - framed-balloon-blue.svg
       - framed-balloon-indigo.svg _(shortcut to framed-balloon-blue.svg)_
       - framed-balloon-red.svg
       - framed-balloon-rouge.svg _(shortcut to framed-balloon-red.svg)_
     - 64/
       - framed-balloon.svg _(shortcut to framed-balloon-red.svg)_
       - framed-balloon-adaptive.svg
       - framed-balloon-blue.svg
       - framed-balloon-indigo.svg _(shortcut to framed-balloon-blue.svg)_
       - framed-balloon-red.svg
       - framed-balloon-rouge.svg _(shortcut to framed-balloon-red.svg)_

```ini
aliases=
    framed-balloon,
    framed-balloon-rouge
```
Aliases are a comma-separated list of alternate names the icon will go by. In
the above list you'll see that several icons are shortcuts. This is used when
several different things share the same icon under different names.

For readability, if an icon has several aliases you may want to write one alias
per line. If doing this you must indent additional lines.

```ini
template=template/picture-frame
```
Every icon requires one template. The template is base file which any
modifications or additions are built on. All paths specified in recipes are
relative to the location of the cookbook, it is reccomended templates be kept
in a folder named "templates".

Every template file must have a suffix corrosponding to the size of the icon,
being built. This means one template is required for each size specified in the cookbook. In this example two template files are required:
 - src/templates/picture-frame.32.svg, and
 - src/templates/picture-frame.64.svg

```ini
replace["#frame-contents"]=emblems/balloon
```
Very frequently icons will be built from several parts, not just the base
templates. You may list as many replacements as you need, and replacements will
be done in the order they are written.

Replacements use CSS selectors. In this case `#frame-contents` is the selector.
It's possible for one `replace` recipe to do multiple replacements. The only
limitation to replacements is that replacements must have unique selectors.
There is no limit to how simple or complex a selector can be, but it's generally
advised selectors be kept simple for readability.

One limitation of the replace command is that it only works on `rect` elements
in the SVG file. This is because the replace command uses the position and size
of the rectangle to place in the new contents.

The value of the replacement is the SVG file to be inserted at the location of
the rect. In this case it's `emblems/balloon`. Just like the template, the value
is a path relative to the cookbook, and has a numeric size suffix in the
filename. Unlike the template, the size of the replacement is done according to
the **width** of the **rect** element. If a rect is 28 pixels wide, then in this
case the file to be inserted would be "emblems/balloon.28.svg". It is
reccomended you standardise your sizes somewhat for maximum recyclability.

```ini
attr["#balloon"]["fill"]="@common-red"
```
When building icons you'll commonly want to set element attributes. Most
commonly you'll probably want to change fill colours, but any attribute can
be set.

The first value (in this case, `#balloon`) is the CSS selector for elements you
want to modify. The second (in this case, `fill`) is the attribute you want to
set. The last value (in this case, `@common-red`) is the new attribute value.

Also in this case `@common-red` is one of our `CookbookColors`, so "#FF0000"
will be inserted into the balloon fill colour, making it a red balloon. If you
expect to use a specific color several times it's reccomended you give it a
memorable name and put it in `CookbookColors`.

Note that if an attribute already exists, it will be completly replaced.

```ini
classes["#balloon"]="+ColorScheme-Highlight"
```
When working heavily with dynamic icons, CSS classes are very frequently used.
At the same time, the `attr` recipe may not be appropriate as one element may
have several classes, and you may only want to change a couple.

Just like `replace` and `attr` you'll see we're using CSS selectors (in this
case, `#balloon`) to find what elements we plan to update. The value for
classes is a comma-separated list of classes, classes starting with a `-` will
be removed. For a more complete example:

```ini
classes["#primary-color"]="-ColorScheme-Highlight,ExScheme-Grey-3"
```

The above instruction will remove the `ColorScheme-Highlight` class from the
element `#primary-color`, while also adding the class `ExScheme-Grey-3`.


## Utility Scripts

Breeze icons come with several python scripts which assist in the development of
icons. These scripts are designed for icons built with the Inkscape vector
graphics editor. While other editors should work just fine, you may experience
unexpected results if a different graphics application is used.

Below is a summary of available scripts and their basic usage.

###### compile.py
 - Can be executed directly (ensure permissions are correctly set)
 - Can be used in the command line. Accepts a list of "cookbooks" which will be
   built. `"cookbook.py src/myrecipes.cookbook.ini"`
 - If no cookbooks are specified compile.py will build all cookbooks
   in the src/ directory.

###### prepare.py
- Can be executed directly (ensure permissions are correctly set)
- Can be used in the command line. Accepts a list of SVG files which to be
  prepared. If the SVG file is not present, a new blank SVG file will be
  created. `"prepare.py src/emblems/my-new-glyph.32.svg"`
- Requires a preparation file. Defaults to `"src/_iconoclast-prepare.spec.ini"`.
  This file specifies how components are prepared, based on their folder and
  size.
- `NOTE:` prepare.py performs potentially destructive actions, and directly
  modifies SVG files.

###### optimize.py
 - Can be executed directly (ensure permissions are correctly set)
 - Can be used in the command line. Accepts a list of SVG files to be optimised.
 - If executed directly or no SVG files are listed, this will scan the build/
   folder and optimise all found SVG files.

###### validate.py
 - Used in command-line only. Accepts up to two parameters; the first is the
   file to validate, the second optional argument is a PNG image for comparison.
 - Outputs validation tests performed on an icon.

###### symbolic.py
 - Can be executed directly (ensure permissions are correctly set)
 - Command-line requires an input icon and a destination. Will take one
   monochrome icon and save it as a GTK-friendly symbolic icon.
 - If called directly, will use `"src/_iconoclast-gtk.spec.ini"` to locate
   and configure symbolic icons for GTK.
 - Reccomended to be used on built icons as a final step.

###### build.py
 - Can be executed directly (ensure permissions are correctly set)
 - Creates a log file "build.log" with a report of the build.
 - Is configured using `"src/_iconoclast-build.spec.ini"`
 - The build process will always complete, even if there are errors. You will
   be given a warning in command-line if errors are present. It is always
   reccomended you view the build log, if issues are present it will be stated
   at the beginning of the log.
 - build.py uses the other utility scripts to fully build the icon set,
   built icons will be present in the build/ folder.

##### Other python files
There are several other python files present. These are not used directly, being
helpers to the other working scripts.

## The Icons Folder
Contents of the icons/ folder are copied into the build folder. SVG icons will
be passed through the optimiser. Other files, including configuration, licences,
and author files are copied without additional processing.

Icons in this folder take precedence over generated icons.

## SVG Limitations
Desktop icons in KDE use an SVG specification called "TinySVG 1.2 Static". This
is a limited subset of SVG meant to perform well under constrained conditions.
The scripts are targeted towards this specification, and may remove unsupported
formatting found in icon files without warning.

## Issues

To report a bug or request new icons, use the
[KDE Bugtracker](https://bugs.kde.org/enter_bug.cgi?product=Breeze&component=Icons).

## Contribute

You can contact the KDE Visual Design Group at the following places:

- `#visualdesigngroup:kde.org` on Matrix: <https://webchat.kde.org/#/room/#kde-vdg:kde.org>
- `#kde-vdg` on Libera Chat IRC
- The VDG Telegram room: <https://telegram.me/vdgmainroom>
- The visual-design@kde.org mailing list: <https://mail.kde.org/mailman/listinfo/visual-design>
