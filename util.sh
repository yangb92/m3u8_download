ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i test.m3u8 -c copy -bsf:a aac_adtstoasc MIE.mp4