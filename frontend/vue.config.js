const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    // Разрешить все хосты (включая my.tuna.am)
    allowedHosts: 'all',
    
    // ИЛИ для большей безопасности явно указать домены:
    // allowedHosts: ['.my.tuna.am', 'localhost'],
    
    // Настройки CORS (если фронт и бекенд на разных доменах)
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': '*'
    },
    
    // Другие возможные параметры:
    host: '0.0.0.0', // Доступ с любого IP
    port: 8080,      // Порт (можно изменить)
    https: false     // HTTPS (true если нужен)
  }
})
