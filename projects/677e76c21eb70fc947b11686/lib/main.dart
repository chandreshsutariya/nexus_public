```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'services/auth_service.dart';
import 'screens/home_screen.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => AuthService()),
        // add other providers here
      ],
      child: MaterialApp(
        title: 'Swiggy Clone',
        theme: ThemeData(primarySwatch: Colors.green),
        home: Consumer<AuthService>(
          builder: (context, authService, _) {
            return authService.isAuthenticated ? HomeScreen() : LoginScreen();
          },
        ),
        routes: {
          '/home': (context) => HomeScreen(),
          '/login': (context) => LoginScreen(),
          // add other routes here
        },
      ),
    );
  }
}
```