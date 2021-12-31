# websocket-audio-stream
pyaudio &amp; websocket to stream real-time audio to speakers or record to wav file.

Works with FreeSWITCH [mod_audio_fork](https://github.com/drachtio/drachtio-freeswitch-modules/blob/main/modules/mod_audio_fork/README.md)

```xml
    <extension name="ws_stream_audio">
      <condition field="destination_number" expression="^stream_audio$">
        <action application="set" data="api_on_answer=uuid_audio_fork ${uuid} start http://localhost:2700 mono 8k 'my custom payload'"/>
        <action application="answer"/>
        <action application="park"/>
      </condition>
    </extension>
```
