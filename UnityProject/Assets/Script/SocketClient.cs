using UnityEngine;
using System;
using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using Leap.Unity.Interaction;

public class SocketClient : MonoBehaviour
{

    // Use this for initialization

    public GameObject hero;
    public GameObject leftHand;
    public GameObject rightHand;

    private float xPos, zPos = 10.0f;
    public int xRot, yRot, zRot = 0;
    private float yPos = 0.055f;
    public string color;

    public float left_x, left_y, left_z;
    public float right_x, right_y, right_z;
    public float distance_Hands, leftDistanceToObj, rightDistanceToObj;

    public static float minHandtoHand = 0.461f;
    public static float minObjtoHand = 0.284f;

    private InteractionController interactionController;

    Thread receiveThread;
    UdpClient client;
    public int port;

    //info

    public string lastReceivedUDPPacket = "";
    public string allReceivedUDPPackets = "";

    void Start()
    {
        init();
        interactionController = (InteractionController)interactionController.GetComponent(typeof(InteractionController));
        print("grasp" + interactionController.Grasp);
    }

    void OnGUI()
    {
        Rect rectObj = new Rect(40, 10, 200, 400);

        GUIStyle style = new GUIStyle();

        style.alignment = TextAnchor.UpperLeft;

        GUI.Box(rectObj, "# UDPReceive\n127.0.0.1 " + port + " #\n"

                  //+ "shell> nc -u 127.0.0.1 : "+port +" \n"

                  + "\nLast Packet: \n" + lastReceivedUDPPacket

                  //+ "\n\nAll Messages: \n"+allReceivedUDPPackets

                  , style);

    }

    private void init()
    {
        print("UPDSend.init()");

        port = 5065;

        print("Sending to 127.0.0.1 : " + port);

        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();


    }

    private void ReceiveData()
    {
        client = new UdpClient(port);
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("127.0.0.1"), port);
                byte[] data = client.Receive(ref anyIP);
                //string text = BitConverter.ToString(data).Replace("-", string.Empty);
                string text = Encoding.UTF8.GetString(data);
                //print(">> " + text);
                lastReceivedUDPPacket = text;
                allReceivedUDPPackets = allReceivedUDPPackets + text;

                //process the string
                // Remove the parentheses
                if (text.StartsWith("(") && text.EndsWith(")"))
                {
                    text = text.Substring(1, text.Length - 2);
                }
                print(text);
                // split the items
                string[] sArray = text.Split(',');

                //get the color
                color = sArray[0];

                if (color == "pink")
                {
                    xRot = 0;
                    yRot = 0;
                    zRot = 0;
                }
                else if (color == "red")
                {
                    xRot = 0;
                    yRot = 0;
                    zRot = 90;
                }
                else if (color == "blue")
                {
                    xRot = 0;
                    yRot = 0;
                    zRot = -90;
                }
                else if (color == "orange")
                {
                    xRot = 90;
                    yRot = 0;
                    zRot = 0;
                }
                else {
                    xRot = 180;
                    yRot = 0;
                    zRot = 0;
                }

                // store as a Vector3
                xPos = float.Parse(sArray[1]);
                xPos -= 320f;
                xPos *= -0.000567f;
                xPos += 9.515f;
                zPos = float.Parse(sArray[2]);
                zPos -= 240f;
                zPos *= 0.000567f;
                zPos += 0.332f;
                yPos = float.Parse(sArray[3]);
                //yPos = 293f - yPos;
                //yPos *= 0.000865f;
                //yPos += 1.6958f;
            }
            catch (Exception e)
            {
                print(e.ToString());
            }
        }
    }

    public string getLatestUDPPacket()
    {
        allReceivedUDPPackets = "";
        return lastReceivedUDPPacket;
    }

    // Update is called once per frame
    void Update()
    {
        
        hero.transform.rotation = Quaternion.Euler(new Vector3(xRot, yRot, yRot));
        hero.transform.position = new Vector3(xPos, 1.6958f, zPos);

        //get the position of both hand
        left_x = leftHand.transform.position.x;
        left_y = leftHand.transform.position.y;
        left_z = leftHand.transform.position.z;
        right_x = rightHand.transform.position.x;
        right_y = rightHand.transform.position.y;
        right_z = rightHand.transform.position.z;

        //distance
        distance_Hands = Vector3.Distance(leftHand.transform.position, rightHand.transform.position);
        leftDistanceToObj = Vector3.Distance(leftHand.transform.position, hero.transform.position);
        rightDistanceToObj = Vector3.Distance(rightHand.transform.position, hero.transform.position);
        //print(distance_Hands + "," + leftDistanceToObj + "," + rightDistanceToObj);

        /*
        if (rightDistanceToObj < minObjtoHand)
        {
            //hero.transform.position = new Vector3(right_x, right_y, right_z);
            print("hold");
        }
        else {
            
            print("left");
        }
        */
    }

    void OnApplicationQuit()
    {
        if (receiveThread != null)
        {
            receiveThread.Abort();
            Debug.Log(receiveThread.IsAlive); //must be false
        }
    }
}
