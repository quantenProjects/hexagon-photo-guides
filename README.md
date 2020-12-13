# hexagon-photo-guides

Scripts to add hexagon marks to photos in order to print, cut them to hexagons and stick them to the wall

## Why?

[Hexagons are the Bestagons](https://www.youtube.com/watch?v=thOifuHs6eY)

# Usage

## Margin Test

For best results, the cutting margin should be known. See [measurments.md](measurments.md) for existing values.

If your favorite printing service is not listed yet, you have to check them your self.

Use the `./create_standard_test_images.sh` script to generate a set of useful test images with a ratio of 36/25.4 (classic size for 18x~~13~~12.7cm at fotoparadies.de). If your service is using another ratio, you may need to use other sizes.

Let them print the test images and measure the margin with the marking. Then, add them to [measurements.md](measurements.md) and make a PR :)

## Add Guides

You can just call `add_guides` with a filename and get centered hexagon markings.

However, you may want some more control:

* `-p`, `--preset`
  * In order to make the process easier, presets for the resolution and cutting margin can be added to the program.
  * The program will choose the resolution (and corresponding cutting margin) with the lowest difference in height.
  * Use `-p list` (and any file) to list all known presets.
* `-r`, `--force-resolution`
  * As the cutting margin will probably vary with the resolution, you want a fixed resolution for printing. This scale the image to the given height. Then it will either crop the image to the ratio of the specified size or adds white space left and right of the image.
  * Example `-r 3600x2540`
* `-c`, `--cutting-margin`
  * Since the hexagon markings will use the full height of the image and many printers/services will crop the images a bit, you may end up with not perfect hexagons. Therefore you can specify the margin in pixels, which will not be used for the hexagon
  * The margin is specified comma separated in the order top, right, bottom, left.
  * Example `-c 19,49,35,53`
* `-g`, `--gui`
  * Since your subject is maybe not centered on the image, you want to change the horizontal positions of the guides. Therefore you can launch a GUI. You have to specify the width of the preview in pixels
  * Click or drag on the image to move the markings. Close the window to accept the position. Watch out for the borders!
  * Example `-g 1024`

If you want to mark a set of photos, a bash for-loop will make things easier:

```bash
for i in *.JPG
do
	echo $i
	python ./add_guides.py -g 1024 -r 3600x2540 -c 19,49,35,53 $i
done
```

```bash
for i in *.JPG
do
	echo $i
	python ./add_guides.py -p dm_fotoparadies_labor $i
done
```

Then print the images and cut along the markings. Now you should have hexagons to stick onto you wall, build honeycombs or what ever. Have Fun!