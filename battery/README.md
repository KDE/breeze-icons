# Battery Icons

Battery icons exist in many versions:

* Different charge levels (0 to 100 in steps of 10)
* Plugged and unplugged
* Different power profiles

The icons share many elements and therefore making them all by hand would be a
lot of work. The script `generate-battery.py` can be used to generate them from
the basic ingredients stored in this folder.

A battery icon is a combination of up to four ingredients:

1. The base icon for the charge level, stored directly in the `icons/status` folder.
2. Another icon added on top of the base to represent the charging status.
3. A third icon representing the power profile, typically in the bottom right corner.
4. A clipping mask used to remove the base icon around the profile icon.

As an example, here are the ingredients going into `icons/status/32/battery-050-charging-profile-powersave.svg`:

|               | Icon          | Path                                                          |
| ------------- | ------------- | ------------------------------------------------------------- |
| Base icon     | ![][base]     | `/icons/status/32/battery-050.svg`                            |
| Charging plug | ![][charging] | `/battery/32/charging.svg`                                    |
| Profile icon  | ![][profile]  | `/battery/32/powersave.svg`                                   |
| Clipping mask | ![][clip]     | `/battery/32/powersave-clip.svg`                              |
| Result        | ![][result]   | `/icons/status/32/battery-050-charging-profile-powersave.svg` |

[base]:     /icons/status/32/battery-050.svg
[charging]: /battery/32/charging.svg
[profile]:  /battery/32/powersave.svg
[clip]:     /battery/32/powersave-clip.svg
[result]:   /icons/status/32/battery-050-charging-profile-powersave.svg

All these inputs are passed to the script as options. A typical invocation is as follows:

```sh
python generate-battery.py --charging battery/22/charging.svg \
                           --profile powersave \
                           --profile-clip battery/22/powersave-clip.svg \
                           --profile-emblem battery/22/powersave.svg \
                           --profile-translate-charging " -3,0" \
                           icons/status/22/battery-000.svg
```

This would take the base icon from `icons/status/22/battery-000.svg` and generate
`icons/status/22/battery-000-profile-powersave.svg` and `icons/status/22/battery-000-charging-profile-powersave.svg`.
The name of the icon is taken from the `--profile` option. The charging symbol
is taken from `--charging`, the profile icon from `--profile-emblem` and the
clipping path around it from `--profile-clip`.

The script assumes that each icon file contains a single SVG `<path>` element.
Using groups, ellipses, or rectangles will not work.

As a special feature, the script can also translate the charging icon when there
is a profile icon so they don't overlap. This is specified by the
`--profile-translate-charging` option, which specifies X and Y coordinates in
pixels (an additional space is needed at the beginning to prevent it being
interpreted as an option). Currently, 16px icons use `" -2,0"` and 22px icons
use `" -3,0"`.

The script needs Inkscape (tested with 1.3.2) and Scour (0.38.2). If they aren't
available directly in `PATH` (as is the case e.g. for Flatpak installs), one can
pass their location or that of a wrapper script using the `--inkscape` and
`--scour` arguments.

## Commands to reproduce existing icons

The following commands can be used to reproduce all profile icons in the repository:

```sh
python generate-battery.py --charging battery/32/charging.svg \
                           --profile powersave \
                           --profile-clip battery/32/powersave-clip.svg \
                           --profile-emblem battery/32/powersave.svg \
                           icons/status/32/battery-{000,010,020,030,040,050,060,070,080,090,100}.svg

python generate-battery.py --charging battery/22/charging.svg \
                           --profile powersave \
                           --profile-clip battery/22/powersave-clip.svg \
                           --profile-emblem battery/22/powersave.svg \
                           --profile-translate-charging " -3,0" \
                           icons/status/22/battery-{000,010,020,030,040,050,060,070,080,090,100}.svg

python generate-battery.py --charging battery/16/charging.svg \
                           --profile powersave \
                           --profile-clip battery/16/powersave-clip.svg \
                           --profile-emblem battery/16/powersave.svg \
                           --profile-translate-charging " -2,0" \
                           icons/status/16/battery-{000,010,020,030,040,050,060,070,080,090,100}.svg


python generate-battery.py --charging battery/32/charging.svg \
                            --profile balanced \
                            --profile-clip battery/32/balanced-clip.svg \
                            --profile-emblem battery/32/balanced.svg \
                            icons/status/32/battery-{000,010,020,030,040,050,060,070,080,090,100}.svg

python generate-battery.py --charging battery/22/charging.svg \
                            --profile balanced \
                            --profile-clip battery/22/balanced-clip.svg \
                            --profile-emblem battery/22/balanced.svg \
                            --profile-translate-charging " -3,0" \
                            icons/status/22/battery-{000,010,020,030,040,050,060,070,080,090,100}.svg

python generate-battery.py --charging battery/16/charging.svg \
                            --profile balanced \
                            --profile-clip battery/16/balanced-clip.svg \
                            --profile-emblem battery/16/balanced.svg \
                            --profile-translate-charging " -2,0" \
                            icons/status/16/battery-{000,010,020,030,040,050,060,070,080,090,100}.svg


python generate-battery.py --charging battery/32/charging.svg \
                            --profile performance \
                            --profile-clip battery/32/rocket-clip.svg \
                            --profile-emblem battery/32/rocket.svg \
                            icons/status/32/battery-{000,010,020,030,040,050,060,070,080,090,100}.svg

python generate-battery.py --charging battery/22/charging.svg \
                            --profile performance \
                            --profile-clip battery/22/rocket-clip.svg \
                            --profile-emblem battery/22/rocket.svg \
                            --profile-translate-charging " -3,0" \
                            icons/status/22/battery-{000,010,020,030,040,050,060,070,080,090,100}.svg

python generate-battery.py --charging battery/16/charging.svg \
                            --profile performance \
                            --profile-clip battery/16/rocket-clip.svg \
                            --profile-emblem battery/16/rocket.svg \
                            --profile-translate-charging " -2,0" \
                            icons/status/16/battery-{000,010,020,030,040,050,060,070,080,090,100}.svg
```
