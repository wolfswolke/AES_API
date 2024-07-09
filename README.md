# AES_API
API for hosting Unreal Engine PAK Encryption keys.

This tool was made with FModel in mind but the FModel integration is not finished yet.

The API is hosted at: https://aes.zkwolf.com/

## Using the API

### Get a list of all games
The Game list is hosted under https://aes.zkwolf.com/api/v1/aes/

### Register a User.
If you want to add a new game you need to register a user.
* go to https://aes.zkwolf.com/profile and register a user.
* Copy your "token"
* With a tool like Postman or insomnia POST a new game!

### POST a new game
Games are hosted under https://aes.zkwolf.com/api/v1/aes/

To add a new game POST a request to that URL with the GameName after the slash.

```
POST https://aes.zkwolf.com/api/v1/aes/HYENAS
{
   "dynamicKeys":[],
   "mainKey":"0x35BA3129A49E9E0372E3401BB50A6A808E6C5B60DCC2D339C390B4C0C494BD43",
   "unloaded":[],
   "version":"0"
}
```

If your game has multiple keys you can add them to the dynamicKeys array.

```
POST https://aes.zkwolf.com/api/v1/aes/HYENAS
{
   "dynamicKeys":[
      {
         "guid":"00000000-00000000-00000000-00000000",
         "key":"0x35BA3129A49E9E0372E3401BB50A6A808E6C5B60DCC2D339C390B4C0C494BD43",
         "name":"pakchunk0-WindowsClient.pak"
      }
   ],
   "mainKey":"0x35BA3129A49E9E0372E3401BB50A6A808E6C5B60DCC2D339C390B4C0C494BD43",
   "unloaded":[
      
   ],
   "version":"0.1"
}
```

### GET a game
To get a game you can use the same URL but with GET and no body.

```
GET https://aes.zkwolf.com/api/v1/aes/HYENAS
```

## TODO
* Finish FModel integration
* Add a way to update games (include HTML)
* Add a way to delete games (include HTML)
* Add a HTML page to add games
* Make the HTML look better (a lot...)