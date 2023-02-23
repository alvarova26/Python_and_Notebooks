#!/bin/bash

sudo date > /tmp/output_script_curl.txt
echo "Init" >> /tmp/output_script_curl.txt
echo -e 'cLBA/cLB/cProbe\t\t\t Response\n' >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a08d10162cb0b4d088508a31ee33e032-19e7aad28208e100.elb.us-east-1.amazonaws.com/1131/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-clb-1131-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a08d10162cb0b4d088508a31ee33e032-19e7aad28208e100.elb.us-east-1.amazonaws.com/1101/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-clba-1101-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a08d10162cb0b4d088508a31ee33e032-19e7aad28208e100.elb.us-east-1.amazonaws.com/1102/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-clba-1102-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a08d10162cb0b4d088508a31ee33e032-19e7aad28208e100.elb.us-east-1.amazonaws.com/1141/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-cprobe-1141-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a08d10162cb0b4d088508a31ee33e032-19e7aad28208e100.elb.us-east-1.amazonaws.com/1142/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-cprobe-1142-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a08d10162cb0b4d088508a31ee33e032-19e7aad28208e100.elb.us-east-1.amazonaws.com/1143/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-cprobe-1143-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a08d10162cb0b4d088508a31ee33e032-19e7aad28208e100.elb.us-east-1.amazonaws.com/1144/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-cprobe-1144-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a9db0b59529e249919809c8f21d0dbb6-dc195cc63a3b2d57.elb.us-east-2.amazonaws.com/1231/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-clb-1231-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a9db0b59529e249919809c8f21d0dbb6-dc195cc63a3b2d57.elb.us-east-2.amazonaws.com/1201/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-clba-1201-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a9db0b59529e249919809c8f21d0dbb6-dc195cc63a3b2d57.elb.us-east-2.amazonaws.com/1202/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-clba-1202-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a9db0b59529e249919809c8f21d0dbb6-dc195cc63a3b2d57.elb.us-east-2.amazonaws.com/1241/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-cprobe-1241-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a9db0b59529e249919809c8f21d0dbb6-dc195cc63a3b2d57.elb.us-east-2.amazonaws.com/1242/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-cprobe-1242-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a9db0b59529e249919809c8f21d0dbb6-dc195cc63a3b2d57.elb.us-east-2.amazonaws.com/1243/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-cprobe-1243-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://a9db0b59529e249919809c8f21d0dbb6-dc195cc63a3b2d57.elb.us-east-2.amazonaws.com/1244/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-cprobe-1244-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://aecb9ad403f5348418c41fd69d744f12-b4c6697d717d15f7.elb.us-west-2.amazonaws.com/1331/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-clb-1331-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://aecb9ad403f5348418c41fd69d744f12-b4c6697d717d15f7.elb.us-west-2.amazonaws.com/1301/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-clba-1301-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://aecb9ad403f5348418c41fd69d744f12-b4c6697d717d15f7.elb.us-west-2.amazonaws.com/1302/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-clba-1302-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://aecb9ad403f5348418c41fd69d744f12-b4c6697d717d15f7.elb.us-west-2.amazonaws.com/1341/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-cprobe-1341-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://aecb9ad403f5348418c41fd69d744f12-b4c6697d717d15f7.elb.us-west-2.amazonaws.com/1342/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-cprobe-1342-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://aecb9ad403f5348418c41fd69d744f12-b4c6697d717d15f7.elb.us-west-2.amazonaws.com/1343/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-cprobe-1343-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://aecb9ad403f5348418c41fd69d744f12-b4c6697d717d15f7.elb.us-west-2.amazonaws.com/1344/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-cprobe-1344-0\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ada7cfb51732644f5b6f5e828be9d4c9-1526046953.us-east-1.elb.amazonaws.com/2001/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az2-clba-2001\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ada7cfb51732644f5b6f5e828be9d4c9-1526046953.us-east-1.elb.amazonaws.com/2002/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az2-clba-2002\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ada7cfb51732644f5b6f5e828be9d4c9-1526046953.us-east-1.elb.amazonaws.com/2031/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az2-clb-2031\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ada7cfb51732644f5b6f5e828be9d4c9-1526046953.us-east-1.elb.amazonaws.com/2041/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az2-cprobe-2041\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ada7cfb51732644f5b6f5e828be9d4c9-1526046953.us-east-1.elb.amazonaws.com/2042/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az2-cprobe-2042\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ada7cfb51732644f5b6f5e828be9d4c9-1526046953.us-east-1.elb.amazonaws.com/2043/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az2-cprobe-2043\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ada7cfb51732644f5b6f5e828be9d4c9-1526046953.us-east-1.elb.amazonaws.com/2044/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az2-cprobe-2044\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-abb15423959164c76979434664aae03e-643888667.us-east-1.elb.amazonaws.com/2101/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az4-clba-2101\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-abb15423959164c76979434664aae03e-643888667.us-east-1.elb.amazonaws.com/2102/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az4-clba-2102\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-abb15423959164c76979434664aae03e-643888667.us-east-1.elb.amazonaws.com/2131/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az4-clb-2131\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-abb15423959164c76979434664aae03e-643888667.us-east-1.elb.amazonaws.com/2141/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az4-cprobe-2141\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-abb15423959164c76979434664aae03e-643888667.us-east-1.elb.amazonaws.com/2142/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az4-cprobe-2142\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-abb15423959164c76979434664aae03e-643888667.us-east-1.elb.amazonaws.com/2143/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az4-cprobe-2143\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-abb15423959164c76979434664aae03e-643888667.us-east-1.elb.amazonaws.com/2144/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e1-az4-cprobe-2144\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-aa8bd38a3d0264b47885709af1bfb42d-1062093061.us-east-2.elb.amazonaws.com/2201/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az1-clba-2201\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-aa8bd38a3d0264b47885709af1bfb42d-1062093061.us-east-2.elb.amazonaws.com/2202/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az1-clba-2202\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-aa8bd38a3d0264b47885709af1bfb42d-1062093061.us-east-2.elb.amazonaws.com/2231/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az1-clb-2231\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-aa8bd38a3d0264b47885709af1bfb42d-1062093061.us-east-2.elb.amazonaws.com/2241/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az1-cprobe-2241\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-aa8bd38a3d0264b47885709af1bfb42d-1062093061.us-east-2.elb.amazonaws.com/2242/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az1-cprobe-2242\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-aa8bd38a3d0264b47885709af1bfb42d-1062093061.us-east-2.elb.amazonaws.com/2243/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az1-cprobe-2243\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-aa8bd38a3d0264b47885709af1bfb42d-1062093061.us-east-2.elb.amazonaws.com/2244/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az1-cprobe-2244\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a7710f093e93048939dc225f333bdb25-1349420147.us-east-2.elb.amazonaws.com/2301/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az2-clba-2301\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a7710f093e93048939dc225f333bdb25-1349420147.us-east-2.elb.amazonaws.com/2302/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az2-clba-2302\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a7710f093e93048939dc225f333bdb25-1349420147.us-east-2.elb.amazonaws.com/2331/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az2-clb-2331\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a7710f093e93048939dc225f333bdb25-1349420147.us-east-2.elb.amazonaws.com/2341/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az2-cprobe-2341\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a7710f093e93048939dc225f333bdb25-1349420147.us-east-2.elb.amazonaws.com/2342/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az2-cprobe-2342\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a7710f093e93048939dc225f333bdb25-1349420147.us-east-2.elb.amazonaws.com/2343/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az2-cprobe-2343\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a7710f093e93048939dc225f333bdb25-1349420147.us-east-2.elb.amazonaws.com/2344/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-e2-az2-cprobe-2344\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ab5cb5be6082f41199171663aa88c79d-1556055419.us-west-2.elb.amazonaws.com/2401/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az1-clba-2401\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ab5cb5be6082f41199171663aa88c79d-1556055419.us-west-2.elb.amazonaws.com/2402/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az1-clba-2402\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ab5cb5be6082f41199171663aa88c79d-1556055419.us-west-2.elb.amazonaws.com/2431/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az1-clb-2431\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ab5cb5be6082f41199171663aa88c79d-1556055419.us-west-2.elb.amazonaws.com/2441/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az1-cprobe-2441\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ab5cb5be6082f41199171663aa88c79d-1556055419.us-west-2.elb.amazonaws.com/2442/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az1-cprobe-2442\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ab5cb5be6082f41199171663aa88c79d-1556055419.us-west-2.elb.amazonaws.com/2443/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az1-cprobe-2443\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-ab5cb5be6082f41199171663aa88c79d-1556055419.us-west-2.elb.amazonaws.com/2444/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az1-cprobe-2444\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a0f7de4e96df74aeca31d9b2185537ae-1497336435.us-west-2.elb.amazonaws.com/2501/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az2-clba-2501\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a0f7de4e96df74aeca31d9b2185537ae-1497336435.us-west-2.elb.amazonaws.com/2502/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az2-clba-2502\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a0f7de4e96df74aeca31d9b2185537ae-1497336435.us-west-2.elb.amazonaws.com/2531/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az2-clb-2531\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a0f7de4e96df74aeca31d9b2185537ae-1497336435.us-west-2.elb.amazonaws.com/2541/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az2-cprobe-2541\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a0f7de4e96df74aeca31d9b2185537ae-1497336435.us-west-2.elb.amazonaws.com/2542/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az2-cprobe-2542\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a0f7de4e96df74aeca31d9b2185537ae-1497336435.us-west-2.elb.amazonaws.com/2543/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az2-cprobe-2543\t\t '$curl_resp >> /tmp/output_script_curl.txt
curl_resp=$(curl -ILsm 3 http://internal-a0f7de4e96df74aeca31d9b2185537ae-1497336435.us-west-2.elb.amazonaws.com/2544/monserver/AjaxClient/JSP/Login/Login.jsp --stderr - | grep HTTP)
echo -e 'pro-fe-w2-az2-cprobe-2544\t\t '$curl_resp >> /tmp/output_script_curl.txt
echo "End" >> /tmp/output_script_curl.txt
cat /tmp/output_script_curl.txt
