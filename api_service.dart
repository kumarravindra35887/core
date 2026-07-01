import 'dart:convert';
import 'package:http/http.dart' as http;
import 'api_config.dart';

class ApiService {
  static Future<Map<String, dynamic>> studentLogin({
    required String email,
    required String password,
    required String deviceId,
  }) async {
    try {
      final response = await http.post(
        Uri.parse(ApiConfig.loginUrl),
        body: {
          'email': email,
          'password': password,
          'device_id': deviceId,
        },
      );
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        return {'role': 'ERROR', 'message': 'लॉगिन विफल: ${response.statusCode}'};
      }
    } catch (e) {
      return {'role': 'ERROR', 'message': 'कनेक्शन विफल: $e'};
    }
  }
}
