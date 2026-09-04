import { registerRootComponent } from 'expo';

import App from './App';

// registerRootComponent 는 AppRegistry.registerComponent('main', () => App) 을 호출하고,
// Expo Go / 네이티브 빌드 양쪽에서 동일하게 동작하도록 환경을 맞춰 줍니다.
registerRootComponent(App);
