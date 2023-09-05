import 'dart:math';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image/image.dart' as img;

enum Channel {
  red,
  green,
  blue,
  alpha,
  luminance,
}

class ImageProcessing {
  static Future<MemoryImage> luminanceThreshold({
    required String assetPath,
    double threshold = 0.7,
    bool outputColor = false,
    double amount = 1,
    Uint8List? maskBytes,
    Channel maskChannel = Channel.luminance,
  }) async {
    final ByteData data = await rootBundle.load(assetPath);
    final List<int> bytes = data.buffer.asUint8List();

    final originalImage = img.decodeImage(Uint8List.fromList(bytes))!;

    img.Image? maskImage;
    if (maskBytes != null) {
      maskImage = img.decodeImage(maskBytes);
    }

    final processedImage = img.gaussianBlur(originalImage, radius: 20);
    final processedImage2 = img.luminanceThreshold(processedImage,
        outputColor: false, amount: 1, mask: maskImage);

    final resizedImage = img.copyResize(processedImage2,
        width: 5 * 1,
        height: 13 * 1,
        interpolation: img.Interpolation.average); // Resize the image
    final resizedBytes = Uint8List.fromList(img.encodePng(resizedImage));

    return MemoryImage(resizedBytes);
  }
}

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Image Processing App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('Image Processing Example'),
        ),
        body: Container(
          child: SingleChildScrollView(
            child: Column(
              children: [
                Image.asset(
                    'assets/original_image.png'), // Replace with your asset path
                SizedBox(height: 20),
                ElevatedButton(
                  onPressed: () async {
                    final processedImage =
                        await ImageProcessing.luminanceThreshold(
                      assetPath:
                          'assets/original_image.png', // Replace with your asset path
                      threshold: 0.5,
                      outputColor: true,
                      amount: 1.0,
                    );
                    Navigator.of(context).push(MaterialPageRoute(
                      builder: (_) => Scaffold(
                        appBar: AppBar(title: Text('Processed Image')),
                        body: Center(child: Image(image: processedImage)),
                      ),
                    ));
                  },
                  child: Text('Apply Image Processing'),
                ),
              ],
            ),
          ),
        ));
  }
}
