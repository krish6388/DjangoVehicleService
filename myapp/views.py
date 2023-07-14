import random
from django.shortcuts import render
from django.http import HttpResponse
from .models import Issue, Agents, Mechanic


def create_issue(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        location = request.POST['location']
        problem = request.POST['problem']
        time = request.POST['time']

        issue = Issue.objects.create(
            userID=user_id,
            location=location,
            problem=problem,
            time=time,
            status='INQUEUE'
        )

        assign_agent(issue)

        return HttpResponse('Issue created successfully.')

    return render(request, 'create_issue.html')


def assign_agent(issue):
    agents = Agents.objects.all().order_by('queue')
    agent = agents.first()

    issue.agentId = agent.agentID
    
    issue.save()

    
    if agent.assigned_issues:
        agent.assigned_issues += ',' + str(issue.issueID)
        agent.queue += 1
    else:
        issue.status = 'ASSIGNED'
        issue.save()
        is_assigned = assign_mechanic(issue= issue)
        if is_assigned:
            pass
        else:
            agent.assigned_issues = str(issue.issueID)
            agent.queue += 1
    
    agent.save()


def assign_mechanic(issue):
    available_mechanics = Mechanic.objects.filter(availability=True)
    if available_mechanics:
        mechanic = random.choice(available_mechanics)
        mechanic.availability = False
        mechanic.save()
        issue.status = 'DISPATCHED'
        issue.mechanicId = mechanic.mechanicID
        issue.save()
        return True
    else:
        return False

def resolve_issue(issue_id):
    issue = Issue.objects.filter(issueID= int(issue_id)).first()
    issue.status = 'RESOLVED'
    issue.save()
    mechanic_id = issue.mechanicId
    mechanic = Mechanic.objects.filter(mechanicID=int(mechanic_id)).first()
    mechanic.availability = True
    mechanic.save()
    next_issue = Issue.objects.filter(status='ASSIGNED').order_by('time').first()
    if assign_mechanic(next_issue):
        agent_id = next_issue.agentId
        free_agent(agent_id)

def free_agent(agent_id):
    agent = Agents.objects.filter(agentID=int(agent_id)).first()
    issues = agent.assigned_issues.split(',')
    issues = issues[1:]
    if len(issues) == 0:
        agent.assigned_issues = ''
    else:
        issue_id = int(issues[0])
        issue = Issue.objects.filter(issueID=issue_id).first()
        issue.status = 'ASSIGNED'
        issue.save()
        agent.assigned_issues = ",".join(issues)
    agent.queue -= 1
    agent.save()

def close_issue(request):
    if request.method == 'POST':
        issue_id = request.POST['issue_id']
        ISSUES = Issue.objects.filter(issueID = issue_id).first()
        if not ISSUES:
            return HttpResponse("Please enter a valid issue id.")
        if ISSUES.status == 'RESOLVED':
            return HttpResponse("This issue is already resolved")
        elif ISSUES.status == 'ASSIGNED':
            return HttpResponse("Please wait your issue is assigned to an agent. You will be shortly assisted.")
        else:
            resolve_issue(ISSUES.issueID)
            return HttpResponse("Your issue has been resolved successfully.")


    return render(request, 'close_issue.html')

def home(request):
    return render(request, 'home.html')
