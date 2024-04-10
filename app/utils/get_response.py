from .clinics import *
from langchain.tools import tool
from dotenv import load_dotenv
from .schema import Clinic, ClinicList
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor

load_dotenv(override=True)


@tool
def get_user_info(mobile: str) -> str:
    '''RETURNS THE USER INFO FROM DATABASE FOR THE GIVEN MOBILE NUMBER.'''
    response = str(getUser(mobile))
    return response


@tool
def add_new_user(mobile: str, name: str, address: str) -> str:
    '''ADDS A NEW USER IN THE DATABASE.'''
    response = str(addUser(mobile, name, address))
    return response


@tool
def update_existing_user(mobile: str, name: str, address: str) -> str:
    '''UPDATES AN EXISTING USER IN THE DATABASE.'''
    response = str(updateUser(mobile, name, address))
    return response


@tool
def get_clinics_list(latitude: int, longitude: int, nearest: int) -> ClinicList:
    '''RETURN THE NEAREST CLINIC IN THE DATABASE.GET THE USER COORDINATES FROM DATABASE TO GET THE NEAREST CLINIC.PASS THE NUMBER OF CLINICS YOU WANT TO GET (DEFAULT VALUE IS 1).'''
    clinics = get_clinics(latitude, longitude, nearest)
    return ClinicList(message=clinics, status=200)


@tool
def get_clinic_schedule(clinicId: int) -> str:
    '''RETURNS SOME SCHEDULES OF THE CLINIC FROM DATABASE FOR THE GIVEN CLINIC ID.'''
    print(clinicId)
    response = str(get_Appointment(clinicId))
    print(response)
    return response


@tool
def get_user_appointments(mobile: str) -> str:
    '''RETURNS PENDING AND COMPLETED APPOINTMENTS OF THE USER FROM DATABASE FOR THE GIVEN MOBILE NUMBER.'''
    response = str(get_user_appointments_fromServer(mobile))
    return response


@tool
def add_appointment(mobile: str, clinic: str, date: str, time: str) -> str:
    '''ADDS AN APPOINTMENT FOR THE USER IN THE DATABASE. PROVIDE FULL NAME FOR CLINIC. DATE IS IN yyyy-mm-dd FORMAT.'''
    response = str(add_user_appointment(clinic,  time, mobile, date))
    return response


@tool
def update_user_appoitment(id: str, clinic: str, date: str, time: str) -> str:
    '''UPDATES AN APPOINTMENT FOR THE USER IN THE DATABASE. PROVIDE FULL NAME FOR CLINIC. DATE IS IN yyyy-mm-dd FORMAT.'''
    response = str(update_appointment(id, clinic, date, time))
    return response


tools = [get_clinics_list, get_clinic_schedule,
         get_user_info, get_user_appointments,
         add_appointment, add_new_user,
         update_existing_user, update_user_appoitment]

llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

prompt = hub.pull("hwchase17/openai-functions-agent")

agent = create_openai_functions_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def generate_response(wa_id, name, message_body):
    messages = [
        SystemMessage(
            content=f'''You are a dental clinic appointment schedling chatbot.
            You cant answer anything other than that.
            Use the tools provided to you for:
                getting appointment status for user,
                or showing the user a clinic's schedule,
                or available clinics,
                or booking an appointment for the user,
                or getting the user's info,
                or updating an appointment details like date,time,clinic name etc,
                or getting the user's appointments status like list of completed or pending appointments.

            First check if user is present in database.
            **If user is not found in database, add him using the provided name and number, you have to formally ask for the user address from user only don't assume the address's of user**
            If user wants to update his info, ask him what field he wants to update and then only update that particular field.
            While adding an appointment provide the date in yyyy-mm-dd format.
            While updating an appointment provide the appointment id, clinic name, date and time in the provided format.
            While getting the clinic schedule provide the clinic name.
            Use the chat history to get the previous conversation and provide the response accordingly.
            If the user is new, greet him and provide the information about the bot and the tools available.
            If the user wants to book the appointment , DON'T ASK FOR CLINIC NAME FIRST FROM USER YOU SHOULD PROVIDE THE LIST OF CLINICS FIRST, just provide the list of available clinics and ask the user to select the clinic and then provide the date and time available to book the slot.

            **NOTE:
                DON'T ASSUME THE COORDINATES WHILE GETTING NEAREST CLINICS, ALWAYS GET THE COORDINATES OF USER FROM THE DATABASE ONLY.

            USER'S NAME: {name},
            MOBILE NUMBER: {wa_id[-12:]},
            While replying the information, or the details of the appointment or clinics, provide the information in a structured Format.

            Start by saying greetings to the user and giving a short description that you are a Dental CLinic Appointment scheduler.'''


        ),
    ]

    old_messages = get_conversation(wa_id[-12:])

    for coversation in old_messages:
        messages.append(
            HumanMessage(
                content=coversation["user"]
            )

        )
        messages.append(
            AIMessage(
                content=coversation["bot"]
            )
        )

    response = agent_executor.invoke(
        {
            "input": message_body,
            "chat_history": messages,
        }
    )

    # Return text in uppercase
    resp = str(response["output"])
    add_conversation(wa_id, message_body, resp)

    return resp
