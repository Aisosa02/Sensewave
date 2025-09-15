using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using UnityEngine.Networking;

public class LiveDepthFeed : MonoBehaviour
{
    public RawImage display;            
    public string serverUrl = "http://127.0.0.1:5000/process"; // Laptop IP

    private WebCamTexture camTexture;

    void Start()
    {
        // Start Camera
        camTexture = new WebCamTexture();
        display.texture = camTexture;
        display.material.mainTexture = camTexture;
        camTexture.Play();

        // Send frames to Flask server
        StartCoroutine(SendFrameLoop());
    }

    IEnumerator SendFrameLoop()
    {
        while (true)
        {
            yield return new WaitForSeconds(0.5f); // Send Frequency

            // Capture current frame
            Texture2D tex = new Texture2D(camTexture.width, camTexture.height);
            tex.SetPixels(camTexture.GetPixels());
            tex.Apply();

            byte[] jpgBytes = tex.EncodeToJPG();
            Destroy(tex);

            // Send frame via POST
            WWWForm form = new WWWForm();
            form.AddBinaryData("frame", jpgBytes, "frame.jpg", "image/jpeg");

            using (UnityWebRequest www = UnityWebRequest.Post(serverUrl, form))
            {
                yield return www.SendWebRequest();

                if (www.result == UnityWebRequest.Result.Success)
                {
                    byte[] resultBytes = www.downloadHandler.data;
                    Texture2D overlayTex = new Texture2D(2, 2);
                    overlayTex.LoadImage(resultBytes);
                    display.texture = overlayTex;
                }
                else
                {
                    Debug.LogError("Server error: " + www.error);
                }
            }
        }
    }
}
