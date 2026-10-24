# Media provenance and project scope

## Screenshots and tour

The five Android screenshots were supplied by the project owner for this public showcase. They show Home, Scenarios, Expression Coach, Games and Settings in guest mode. No learner history, camera feed, transcript, credential or private dashboard is shown.

The GIF is a fifteen-second sequence of those screenshots with navigation captions. It is labeled as a screenshot tour rather than a live interaction recording. Original screenshots are retained in `docs/screenshots`.

The architecture SVG and project documentation describe the inspected implementation. This showcase does not include the application source, trained weights, speech-model files or character meshes/textures.

## Third-party technology and artwork context

- React Native and React power the mobile interface.
- Google MediaPipe supplies face/hand landmark tooling.
- TensorFlow Lite and Microsoft ONNX Runtime execute local expression models.
- Vosk supplies offline speech recognition; Android provides device narration.
- Three.js renders the local 3D guide in a React Native WebView.
- The current Ayaan guide uses Rocketbox Male_Child_01, as recorded by the application implementation notes. Screenshots show its rendered appearance; character files are not redistributed here.
- The app includes project-authored gameplay vectors and generated illustration assets. The supplied screenshots depict the resulting interface; illustration source bundles are not redistributed here.

Third-party software, models and character assets retain their respective terms. This repository does not assign a new license to those underlying materials or grant rights to extract them from screenshots.

## Status and interpretation

Expressify AI is an educational prototype, not a diagnostic instrument or a clinically validated treatment. Participation counts, question results and device-reported movement matches have distinct meanings. This repository makes no recognition-accuracy or therapeutic-effect claim.

The product currently targets supported Android use. Native iOS sensing parity, Urdu/RTL, broader intended-user evaluation and public-release operations remain separate work.
