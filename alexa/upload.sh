rm -rf ../alexa.zip
zip -r ../alexa.zip * -x \*aws-sdk\*
cd ..
echo "Uploading..."
aws lambda update-function-code --function-name JamRecorderAlexaSkill --zip-file fileb://alexa.zip
