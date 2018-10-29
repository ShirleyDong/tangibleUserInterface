using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CubeCollision : MonoBehaviour {

	// Use this for initialization
	void Start () {

	}
	
	// Update is called once per frame
	void Update () {

    }
    void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.name == "rbone3") {
            print("get");
        }
    }

    private void OnCollisionExit(Collision collision)
    {
        if (collision.gameObject.name == "rbone3")
        {
            print("exit");
        }
    }
    private void OnCollisionStay(Collision collision)
    {
        if (collision.gameObject.name == "rbone3")
        {
            print("get");
        }
    }
}
