from copy import deepcopy

def data(np):
    # Fast SLAM covariance
    Q = np.diag([3.0, np.deg2rad(10.0)])**2
    R = np.diag([1.0, np.deg2rad(20.0)])**2
    
    #  Simulation parameter
    Qsim = np.diag([0.3, np.deg2rad(2.0)])**2
    Rsim = np.diag([0.5, np.deg2rad(10.0)])**2
    
    return (Q,R,Qsim,Rsim)
#run: log_likelihood(a, b, c)
#from: http://arogozhnikov.github.io/2015/09/08/SpeedBenchmarks.html
numpy = None
#pythran export log_likelihood(float64[], float64, float64)

class Particle:

    def __init__(self, N_LM):
        self.w = 1.0 / N_PARTICLE
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        # landmark x-y positions
        self.lm = np.zeros((N_LM, LM_SIZE))
        # landmark position covariance
        self.lmP = np.zeros((N_LM * LM_SIZE, LM_SIZE))

def motion_model(x, u):
    import math
    F = np.array([[1.0, 0, 0],
                  [0, 1.0, 0],
                  [0, 0, 1.0]])

    B = np.array([[DT * math.cos(x[2, 0]), 0],
                  [DT * math.sin(x[2, 0]), 0],
                  [0.0, DT]])
    x = F @ x + B @ u

    x[2, 0] = pi_2_pi(x[2, 0])
    return x

def predict_particles(particles, u, R):
    for i in range(N_PARTICLE):
        px = np.zeros((STATE_SIZE, 1))
        px[0, 0] = particles[i].x
        px[1, 0] = particles[i].y
        px[2, 0] = particles[i].yaw
        ud = u + (np.random.randn(1, 2) @ R).T  # add noise
        px = motion_model(px, ud)
        particles[i].x = px[0, 0]
        particles[i].y = px[1, 0]
        particles[i].yaw = px[2, 0]

    return particles

def pi_2_pi(angle):
    import math
    return (angle + math.pi) % (2 * math.pi) - math.pi

# END OF SNIPPET

def fastSlam(Q,R,Qsim,Rsim):

    global OFFSET_YAWRATE_NOISE
    OFFSET_YAWRATE_NOISE = 0.01
    
    global DT
    DT = 0.1  # time tick [s]
    global SIM_TIME
    SIM_TIME = 50.0  # simulation time [s]
    global MAX_RANGE
    MAX_RANGE = 20.0  # maximum observation range
    global M_DIST_TH
    M_DIST_TH = 2.0  # Threshold of Mahalanobis distance for data association.
    global STATE_SIZE
    STATE_SIZE = 3  # State size [x,y,yaw]
    global LM_SIZE
    LM_SIZE = 2  # LM srate size [x,y]
    global N_PARTICLE
    N_PARTICLE = 100  # number of particle
    global NTH
    NTH = N_PARTICLE / 1.5  # Number of particle for re-sampling
    
    
    N_LM = 0
    particles = [Particle(N_LM) for i in range(N_PARTICLE)]
    time= 0.0
    v = 1.0  # [m/s]
    yawrate = 0.1  # [rad/s]
    u = np.array([v, yawrate]).reshape(2, 1)
    history = []
    while SIM_TIME >= time:
        time += DT
        particles = predict_particles(particles, u, R)
        history.append(deepcopy(particles))

def func(np, data):
    numpy = np
    fastSlam(*data)
    #return log_likelihood(*data)
