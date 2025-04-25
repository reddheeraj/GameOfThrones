# 🎯 **Game Of Thrones** (prev known as InstaPolitics)
 Game Of Thrones is an agentic sandbox application which simulates how social media influences decisions. 

![image](https://github.com/user-attachments/assets/16c87187-3466-474d-a893-790d2f45ee9e)


** Was initially a hackathon submission, but modified it a lot and made it a class project submission hahahaha
## 🚀 **Inspiration**  
Social media is reshaping modern politics, and InstaPolitics was born to explore that connection! The idea was to create a hands-on simulation where students, especially those in business, education, and political science, can study how politicians sway voters through social media. With InstaPolitics, you can see how political figures craft messages, influence public opinion, and ultimately shape election outcomes in real-time.

---

## 🌍 **What It Does**  
InstaPolitics is a full-stack web app that simulates the complex dynamics of political campaigns and voter behavior. Define personalities for your agents and see them play it out.

- 🏛️ **Politician Agents**: Define unique personalities for political figures, who will post on a **Custom-Built Social Media Platform**.  
- 👥 **Citizen Agents**: Voters react to posts based on their personalities and biases, or decide to not vote. Each move is stored in their own memory.
- 🎯 **Influence and Decision-Making**: Watch how posts influence voters and drive decisions at the ballot box.
- 📊 **Real-Time Simulation**: See political strategies unfold and voter behavior evolve in real-time.
- ✨ **Goal**: To understand how social media shapes modern political influence through direct interaction and dynamic feedback.  

Final look:
---
![image](https://github.com/user-attachments/assets/efe7ea2c-0998-4076-bb20-07968904e09c)


Prototype look:
---
![image](https://github.com/user-attachments/assets/597bf0ba-fd3b-4d33-8fd6-e04f89f06305)


Shows why a particular politician won the elections (based on people's memories):
---
![image](https://github.com/user-attachments/assets/a6646755-5b27-4303-aed1-28042430a87c)


---

## 🛠️ How I Built It
Here's the full-stack architecture breakdown:  

![image](https://github.com/user-attachments/assets/1b681af5-ba45-4cd4-80d4-f8718da2054d)

## 🛠️ **Tech Stack**  

| **Component** | **Tech Used** | **Purpose** |
|-------------|---------------|------------|
| **Frontend** | React, Vite, MaterialUI, Socket.IO | Responsive UI, real-time updates |
| **Backend** | Flask, Python | State management, API handling |
| **Agent Framework** | Customer Framework over Langchain | Decision-making and content generation for agents |
| **Search** | ChromaDB, BM25 | Vector search and ranking for relevance |
| **LLM Support** | Groq, Gemini, Ollama | Generating realistic political content |
| **Real-Time Communication** | Socket.IO | Live updates and interactions |
| **Data Storage** | ChromaDB | Storing embeddings for agent memory and search |
| **Ranking** | BM25 | Ranking social media posts based on influence |
