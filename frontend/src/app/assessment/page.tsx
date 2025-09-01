'use client'

import { motion } from 'framer-motion'
import { useState } from 'react'
import { 
  ChartBarIcon, 
  CurrencyDollarIcon,
  ClockIcon,
  GlobeAltIcon,
  AcademicCapIcon,
  UsersIcon,
  ArrowRightIcon,
  CheckIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'

const fadeInUp = {
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 }
}

const assessmentSteps = [
  {
    id: 'financial',
    title: '财务自由度',
    icon: CurrencyDollarIcon,
    description: '评估你的财务状况和被动收入能力',
    questions: [
      '你的被动收入占总收入的比例是多少？',
      '你有多少个月的应急基金？',
      '你有几种不同的收入来源？'
    ]
  },
  {
    id: 'time',
    title: '时间自由度',
    icon: ClockIcon,
    description: '评估你对时间的控制程度',
    questions: [
      '你的工作时间有多灵活？',
      '你每年有多少天假期？',
      '你能远程工作吗？'
    ]
  },
  {
    id: 'location',
    title: '地理自由度',
    icon: GlobeAltIcon,
    description: '评估你的地理位置限制',
    questions: [
      '你的工作对地点有限制吗？',
      '你多久旅行一次？',
      '你能在任何地方工作吗？'
    ]
  },
  {
    id: 'skill',
    title: '技能自由度',
    icon: AcademicCapIcon,
    description: '评估你的技能可转移性',
    questions: [
      '你的技能在市场上需求如何？',
      '你的技能可以转移到其他行业吗？',
      '你持续学习新技能吗？'
    ]
  },
  {
    id: 'relationship',
    title: '关系自由度',
    icon: UsersIcon,
    description: '评估你的社交网络和情感独立性',
    questions: [
      '你的社交网络有多广泛？',
      '你在情感上独立吗？',
      '你的人际关系质量如何？'
    ]
  }
]

function AssessmentPage() {
  const [currentStep, setCurrentStep] = useState(0)
  const [answers, setAnswers] = useState<Record<string, number>>({})
  const [isCompleted, setIsCompleted] = useState(false)
  const [results, setResults] = useState<Record<string, number>>({})

  const handleAnswer = (questionIndex: number, score: number) => {
    const key = `${assessmentSteps[currentStep].id}_${questionIndex}`
    setAnswers(prev => ({ ...prev, [key]: score }))
  }

  const nextStep = () => {
    if (currentStep < assessmentSteps.length - 1) {
      setCurrentStep(currentStep + 1)
    } else {
      calculateResults()
    }
  }

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const calculateResults = () => {
    const stepResults: Record<string, number> = {}
    
    assessmentSteps.forEach(step => {
      const stepAnswers = Object.entries(answers)
        .filter(([key]) => key.startsWith(step.id))
        .map(([, value]) => value)
      
      if (stepAnswers.length > 0) {
        stepResults[step.id] = Math.round(
          stepAnswers.reduce((sum, score) => sum + score, 0) / stepAnswers.length
        )
      } else {
        stepResults[step.id] = 0
      }
    })
    
    setResults(stepResults)
    setIsCompleted(true)
  }

  const currentStepData = assessmentSteps[currentStep]
  const progress = ((currentStep + 1) / assessmentSteps.length) * 100

  if (isCompleted) {
    const overallScore = Math.round(
      Object.values(results).reduce((sum, score) => sum + score, 0) / Object.values(results).length
    )

    return (
      <div className="min-h-screen bg-gray-900">
        <nav className="starry-navbar">
          <div className="container mx-auto px-4">
            <div className="flex items-center justify-between h-16">
              <Link href="/" className="text-gray-300 hover:text-starry-cyan transition-colors">
                ← 返回首页
              </Link>
              <h1 className="text-xl font-bold text-white">评估结果</h1>
              <div></div>
            </div>
          </div>
        </nav>

        <div className="container mx-auto px-4 py-8">
          <motion.div
            className="text-center mb-12"
            initial="initial"
            animate="animate"
            variants={fadeInUp}
            transition={{ duration: 0.6 }}
          >
            <div className="w-32 h-32 bg-gradient-starry rounded-full flex items-center justify-center mx-auto mb-6">
              <span className="text-4xl font-bold text-white">{overallScore}</span>
            </div>
            <h2 className="text-4xl font-bold text-gradient mb-4">
              你的综合自由度分数
            </h2>
            <p className="text-xl text-gray-300">
              {overallScore >= 80 ? '恭喜！你已经拥有很高的自由度' :
               overallScore >= 60 ? '不错！你在自由的道路上进展良好' :
               overallScore >= 40 ? '还有提升空间，继续努力！' :
               '需要更多努力来提升你的自由度'}
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            {assessmentSteps.map((step, index) => (
              <motion.div
                key={step.id}
                className="starry-card p-6 text-center"
                initial="initial"
                animate="animate"
                variants={fadeInUp}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <step.icon className="w-12 h-12 text-gradient mx-auto mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">{step.title}</h3>
                <div className="text-3xl font-bold text-gradient mb-2">
                  {results[step.id] || 0}%
                </div>
                <div className="starry-progress mb-4">
                  <div 
                    className="starry-progress-bar"
                    style={{ width: `${results[step.id] || 0}%` }}
                  />
                </div>
              </motion.div>
            ))}
          </div>

          <motion.div
            className="text-center"
            initial="initial"
            animate="animate"
            variants={fadeInUp}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            <Link href="/opportunities" className="starry-button mr-4">
              探索机会
            </Link>
            <Link href="/learning" className="starry-button-secondary">
              制定学习计划
            </Link>
          </motion.div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900">
      <nav className="starry-navbar">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="text-gray-300 hover:text-starry-cyan transition-colors">
              ← 返回首页
            </Link>
            <h1 className="text-xl font-bold text-white">自由度评估</h1>
            <div className="text-gray-300">
              {currentStep + 1} / {assessmentSteps.length}
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8">
        {/* 进度条 */}
        <motion.div
          className="mb-8"
          initial="initial"
          animate="animate"
          variants={fadeInUp}
          transition={{ duration: 0.6 }}
        >
          <div className="starry-progress h-3">
            <motion.div 
              className="starry-progress-bar"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
          <p className="text-center text-gray-400 mt-2">
            进度: {Math.round(progress)}%
          </p>
        </motion.div>

        {/* 当前步骤 */}
        <motion.div
          className="starry-card p-8 mb-8"
          initial="initial"
          animate="animate"
          variants={fadeInUp}
          transition={{ duration: 0.6 }}
        >
          <div className="text-center mb-8">
            <currentStepData.icon className="w-16 h-16 text-gradient mx-auto mb-4" />
            <h2 className="text-3xl font-bold text-white mb-4">
              {currentStepData.title}
            </h2>
            <p className="text-gray-300 text-lg">
              {currentStepData.description}
            </p>
          </div>

          <div className="space-y-8">
            {currentStepData.questions.map((question, questionIndex) => (
              <div key={questionIndex} className="space-y-4">
                <h3 className="text-xl text-white font-semibold">
                  {questionIndex + 1}. {question}
                </h3>
                
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">很低</span>
                  <div className="flex space-x-2">
                    {[1, 2, 3, 4, 5].map(score => (
                      <button
                        key={score}
                        onClick={() => handleAnswer(questionIndex, score * 20)}
                        className={`w-12 h-12 rounded-full border-2 transition-all ${
                          answers[`${currentStepData.id}_${questionIndex}`] === score * 20
                            ? 'bg-gradient-starry border-starry-purple text-white'
                            : 'border-gray-600 text-gray-400 hover:border-starry-purple'
                        }`}
                      >
                        {score}
                      </button>
                    ))}
                  </div>
                  <span className="text-gray-400">很高</span>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* 导航按钮 */}
        <motion.div
          className="flex justify-between"
          initial="initial"
          animate="animate"
          variants={fadeInUp}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <button
            onClick={prevStep}
            disabled={currentStep === 0}
            className="starry-button disabled:opacity-50 disabled:cursor-not-allowed"
          >
            上一步
          </button>
          
          <button
            onClick={nextStep}
            disabled={currentStepData.questions.some((_, index) => 
              !answers[`${currentStepData.id}_${index}`]
            )}
            className="starry-button disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {currentStep === assessmentSteps.length - 1 ? (
              <>
                <CheckIcon className="w-5 h-5 inline mr-2" />
                完成评估
              </>
            ) : (
              <>
                下一步
                <ArrowRightIcon className="w-5 h-5 inline ml-2" />
              </>
            )}
          </button>
        </motion.div>
      </div>
    </div>
  )
}

export default AssessmentPage
